python3-logstash
===================

Python logging handler for Logstash.
https://www.elastic.co/products/logstash

Notes:
=========
This is a copy of python3-logstash: https://pypi.python.org/pypi/python3-logstash
That has been update to work with python 3.

Installation
============

Using pip::

  pip install python3-logstash

Usage
=====

``LogstashHandler`` is a custom logging handler which sends Logstash messages using UDP.

For example::

  import logging
  import logstash
  import sys

  host = 'localhost'

  test_logger = logging.getLogger('python3-logstash-logger')
  test_logger.setLevel(logging.INFO)
  test_logger.addHandler(logstash.LogstashHandler(host, 5959, version=1))
  # test_logger.addHandler(logstash.TCPLogstashHandler(host, 5959, version=1))

  test_logger.error('python3-logstash: test logstash error message.')
  test_logger.info('python3-logstash: test logstash info message.')
  test_logger.warning('python3-logstash: test logstash warning message.')

  # add extra field to logstash message
  extra = {
      'test_string': 'python version: ' + repr(sys.version_info),
      'test_boolean': True,
      'test_dict': {'a': 1, 'b': 'c'},
      'test_float': 1.23,
      'test_integer': 123,
      'test_list': [1, 2, '3'],
  }
  test_logger.info('python3-logstash: test extra fields', extra=extra)

When using ``extra`` field make sure you don't use reserved names. From `Python documentation <https://docs.python.org/2/library/logging.html>`_.
     | "The keys in the dictionary passed in extra should not clash with the keys used by the logging system. (See the `Formatter <https://docs.python.org/2/library/logging.html#logging.Formatter>`_ documentation for more information on which keys are used by the logging system.)"

To use the AMQPLogstashHandler you will need to install pika first.

   pip install pika

For example::

  import logging
  import logstash

  test_logger = logging.getLogger('python3-logstash-logger')
  test_logger.setLevel(logging.INFO)
  test_logger.addHandler(logstash.AMQPLogstashHandler(host='localhost', version=1))

  test_logger.info('python3-logstash: test logstash info message.')
  try:
      1/0
  except:
      test_logger.exception('python3-logstash-logger: Exception with stack trace!')



Using with Django
=================

Modify your ``settings.py`` to integrate ``python3-logstash`` with Django's logging::

  LOGGING = {
    ...
    'handlers': {
        'logstash': {
            'level': 'DEBUG',
            'class': 'logstash.LogstashHandler',
            'host': 'localhost',
            'port': 5959, # Default value: 5959
            'version': 1, # Version of logstash event schema. Default value: 0 (for backward compatibility of the library)
            'message_type': 'logstash',  # 'type' field in logstash message. Default value: 'logstash'.
            'fqdn': False, # Fully qualified domain name. Default value: false.
            'tags': ['tag1', 'tag2'], # list of tags. Default: None.
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['logstash'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    ...
  }


Using with Gunicorn
===================

Create a logging.conf similar to this:

[loggers]
keys=root, logstash.error, logstash.access

[handlers]
keys=console , logstash

[formatters]
keys=generic, access, json

[logger_root]
level=INFO
handlers=console

[logger_logstash.error]
level=INFO
handlers=logstash
propagate=1
qualname=gunicorn.error

[logger_logstash.access]
level=INFO
handlers=logstash
propagate=0
qualname=gunicorn.access

[handler_console]
class=logging.StreamHandler
formatter=generic
args=(sys.stdout, )

[handler_logstash]
class=logstash.TCPLogstashHandler
formatter=json
args=('localhost',5959)

[formatter_generic]
format=%(asctime)s [%(process)d] [%(levelname)s] %(message)s
datefmt=%Y-%m-%d %H:%M:%S
class=logging.Formatter

[formatter_access]
format=%(message)s
class=logging.Formatter

[formatter_json]
class=jsonlogging.JSONFormatter

** Note that I am using the jsonlogging module to parse the gunicorn logs **

Sample Logstash Configuration:
==============================

``logstash.conf`` for Receiving Events from python3-logstash is::

  input {
    tcp {
      port => 5000
      codec => json
    }
  }
  output {
    stdout {
      codec => rubydebug
    }
  }

