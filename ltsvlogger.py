# -*- coding: utf-8 -*-
import logging
import time
import datetime

__version__ = '0.9.1'


timestamp = time.time()
tzdelta = datetime.datetime.fromtimestamp(timestamp) - \
    datetime.datetime.utcfromtimestamp(timestamp)


class LocalTimeZone(datetime.tzinfo):

    def __init__(self, *args, **kw):
        super(LocalTimeZone, self).__init__(*args, **kw)
        self.tzdelta = tzdelta

    def utcoffset(self, dt):
        return self.tzdelta

    def dst(self, dt):
        return datetime.timedelta(0)

ltz = LocalTimeZone()


class LTSVFormatter(logging.Formatter):

    default_fields = {
        'asctime': 'time',
        'levelname': 'log_level',
        'message': 'message',
        'name': 'logger_name',
        'process': 'process_id',
        'processName': 'process_name',
        'thread': 'thread_id',
        'threadName': 'thread_name',
    }

    default_datefmt = '%Y-%m-%dT%H:%M:%S%z'

    def __init__(self, fmt=None, datefmt=None, fields=None):
        if fields is None:
            fields = self.default_fields
        if fmt is None:
            fmt = '\t'.join('{1}:%({0})s'.format(*i) for i in fields.items())
        if datefmt is None:
            datefmt = self.default_datefmt
        logging.Formatter.__init__(self, fmt=fmt, datefmt=datefmt)

    def formatTime(self, record, datefmt=None):
        if datefmt is None:
            datefmt = self.default_datefmt

        dt = datetime.datetime.fromtimestamp(time.time(), ltz)

        if '%z' in datefmt:
            z = dt.strftime('%z')
            datefmt = datefmt.replace('%z', '{0}:{1}'.format(z[:-2], z[-2:]))

        return dt.strftime(datefmt)


class LTSVLoggerAdapter(logging.LoggerAdapter):

    def __init__(self, logger):
        logging.LoggerAdapter.__init__(self, logger, {})

    def process(self, msg, kwargs):
        new_kwargs = {}
        for kw in ('exc_info', 'extra'):
            if kw in kwargs:
                new_kwargs[kw] = kwargs.pop(kw)
        if kwargs:
            new_msg = '{0}\t{1}'.format(
                msg,
                '\t'.join('{0}:{1}'.format(*i) for i in kwargs.items()),
            )
        else:
            new_msg = msg
        return new_msg, new_kwargs


def example_logger_setup_by_code():
    formatter = LTSVFormatter(fields={
        'asctime': 'time',
        'user': 'user',
        'host': 'host',
        'message': 'message',
    })

    logger = logging.getLogger('code')
    hdr = logging.StreamHandler()
    hdr.setLevel(logging.INFO)
    hdr.setFormatter(formatter)
    logger.addHandler(hdr)

    # extra keyword argument values fill into format string placeholder.
    # If formatter did not have 'user' and host' placeholder, these
    # values will be simply omitted.
    logger.error(
        'This is a error message with %s',
        'extra arguments',
        extra=dict(
            user='spam',
            host='ham.example.com',
        )
    )


def example_logger_setup_by_code_with_adapter():
    formatter = LTSVFormatter()

    logger = logging.getLogger('adapter')
    hdr = logging.StreamHandler()
    hdr.setLevel(logging.INFO)
    hdr.setFormatter(formatter)
    logger.addHandler(hdr)

    # LTSVLoggerAdapter will extract keyword argument into log format.
    ltsvlogger = LTSVLoggerAdapter(logger)

    ltsvlogger.error(
        'This is a error message with %s',
        'extra arguments',
        user='spam',
        host='ham.example.com',
    )


def example_logger_setup_by_code_with_adapter_no_kwargs():
    formatter = LTSVFormatter()

    logger = logging.getLogger('adapter_no_kwargs')
    hdr = logging.StreamHandler()
    hdr.setLevel(logging.INFO)
    hdr.setFormatter(formatter)
    logger.addHandler(hdr)

    # LTSVLoggerAdapter will extract keyword argument into log format.
    ltsvlogger = LTSVLoggerAdapter(logger)

    ltsvlogger.error(
        'This is a error message without extra arguments'
    )


def example_logger_setup_by_config():
    """
    logger.ini example::

        [loggers]
        keys = root,demo

        [handlers]
        keys = ltsvhdr

        [formatters]
        keys = ltsvfmt

        [logger_root]
        level = DEBUG
        handlers =

        [logger_demo]
        level = DEBUG
        handlers = ltsvhdr
        qualname = demo

        [handler_ltsvhdr]
        class = StreamHandler
        args = (sys.stderr,)
        level = DEBUG
        formatter = ltsvfmt

        [formatter_ltsvfmt]
        format = time:%(asctime)s	logger_name:%(name)s	message:%(message)s
        datefmt = %Y-%m-%dT%H:%M:%S%z
        class = ltsvlogger.LTSVFormatter
    """
    import logging.config
    logging.config.fileConfig('logger.ini')
    logger = logging.getLogger('demo')

    ltsvlogger = LTSVLoggerAdapter(logger)

    ltsvlogger.warning(
        'This is a warning message with %s',
        'keyword arguments',
        user='spam',
        host='ham.example.com',
    )


if __name__ == '__main__':
    example_logger_setup_by_code()
    example_logger_setup_by_code_with_adapter()
    example_logger_setup_by_code_with_adapter_no_kwargs()
    example_logger_setup_by_config()
