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

   formatter = ltsvlogger.LTSVFormatter()

   logger = logging.getLogger('sample')
   hdr = logging.StreamHandler()
   hdr.setLevel(logging.INFO)
   hdr.setFormatter(formatter)
   logger.addHandler(hdr)

   logger.error(
       'This is a error message with %s',
       'extra arguments',
       extra=dict(
           user='spam',
           host='ham.example.com',
       )
   )

   ltsvlogger = LTSVLoggerAdapter(logger)

   ltsvlogger.warning(
       'This is a warning message with %s',
       'keyword arguments',
       user='spam',
       host='ham.example.com',
   )

If you want to change ltsv field, you can setup formatter with field name mapping::

   formatter = ltsvlogger.LTSVFormatter({
       'asctime': 'timestamp',
       'levelname': 'level',
       'message': 'msg',
       'name': 'name',
   })


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
   format = time:%(asctime)s	logger_name:%(name)s	message:%(message)s
   datefmt = %Y-%m-%dT%H:%M:%S%z
   class = ltsvlogger.LTSVFormatter

and use::

   import logging.config
   logging.config.fileConfig('logger.ini')
   logger = logging.getLogger('demo')

   logger.error(
       'This is a error message with %s',
       'extra arguments',
       extra=dict(
           user='spam',
           host='ham.example.com',
       )
   )

   ltsvlogger = LTSVLoggerAdapter(logger)

   ltsvlogger.warning(
       'This is a warning message with %s',
       'keyword arguments',
       user='spam',
       host='ham.example.com',
   )


CHANGES
========

0.9.0 (unreleased)
------------------
First release.

* Provide ltsvlogger.LTSVFormatter
* Provide ltsvlogger.LTSFLoggerAdapter

