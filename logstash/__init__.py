from logstash.formatter import LogstashFormatterVersion0, LogstashFormatterVersion1
from logstash.handler_http import HTTPLogstashHandler
from logstash.handler_tcp import TCPLogstashHandler
from logstash.handler_udp import UDPLogstashHandler

try:
    from logstash.handler_amqp import AMQPLogstashHandler
except:
    # you need to install AMQP support to enable this handler.
    pass

__version__ = "0.5.1"
