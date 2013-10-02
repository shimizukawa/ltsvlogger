=============================================
ltsvlogger : logging with labeled tsv format
=============================================

Basic Features
===============

* Provide ltsvlogger.LTSVFormatter to format ltsv output.
* Provide ltsvlogger.LTSFLoggerAdapter for ease to use.

Requirements
-------------

- Python 2.6, 2.7, 3.2, 3.3, pypy.


Installation
=============

Recommend: use virtualenv for this procedure::

   $ pip install ltsvlogger

If you want to install unreleased version::

   $ pip install https://bitbucket.org/shimizukawa/ltsvlogger/get/tip.zip

Using example
==============

setup logger by code
---------------------

::

   import logging
   import ltsvlogger

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

output sample::

   host:ham.example.com\tmessage:This is a error message with extra arguments\tuser:spam\ttime:2013-09-27T09:21:03+00:00


If you want to output fields in order, you can setup formatter with fmt argument like logging.Formatter parameter::

   formatter = LTSVFormatter(
       'time:%(asctime)s\tuser:%(user)s\thost:%(host)s\tmessage:%(message)s'
   )


setup logger by code with LTSVLoggerAdapter
--------------------------------------------

::

   import logging
   import ltsvlogger

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
       'keyword arguments',
        user='spam',
        host='ham.example.com',
   )


output sample::

   process_name:MainProcess\tlogger_name:sample\tthread_id:140654083024640\ttime:2013-09-27T08:49:53+00:00\tprocess_id:17807\tmessage:This is a error message with keyword arguments\thost:ham.example.com\tuser:spam\tthread_name:MainThread\tlog_level:ERROR


setup logger by config
-----------------------

Prepare logger.ini for logger::

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
   format = time:%(asctime)s\tlogger_name:%(name)s\tmessage:%(message)s
   datefmt = %Y-%m-%dT%H:%M:%S%z
   class = ltsvlogger.LTSVFormatter

and use::

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

output sample::

   time:2013-09-27T08:49:53+00:00\tlogger_name:demo\tmessage:This is a warning message with keyword arguments\thost:ham.example.com\tuser:spam


CHANGES
========

0.9.0 (2013-10-02)
------------------
First release.

* Provide ltsvlogger.LTSVFormatter
* Provide ltsvlogger.LTSFLoggerAdapter

