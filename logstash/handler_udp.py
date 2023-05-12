from logging.handlers import DatagramHandler
from logstash import formatter


class UDPLogstashHandler(DatagramHandler):
    """Python logging handler for Logstash. Sends events over UDP.
    :param host: The host of the logstash server.
    :param port: The port of the logstash server (default 5959).
    :param message_type: The type of the message (default logstash).
    :param fqdn; Indicates whether to show fully qualified domain name or not (default False).
    :param version: version of logstash event schema (default is 0).
    :param tags: list of tags for a logger (default is None).
    """
    def __init__(self, host, port=5959, message_type='logstash', tags=None, fqdn=False, version=0):
        super(UDPLogstashHandler, self).__init__(host, port)
        if version == 1:
            self.formatter = formatter.LogstashFormatterVersion1(message_type, tags, fqdn)
        else:
            self.formatter = formatter.LogstashFormatterVersion0(message_type, tags, fqdn)

    def makePickle(self, record):
        return str.encode(self.formatter.format(record)) + b'\n'


# For backward compatibility
LogstashHandler = UDPLogstashHandler
