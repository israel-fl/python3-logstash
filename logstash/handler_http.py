import logging
import urllib
from base64 import b64encode
from urllib.request import Request

from logstash import formatter


class HTTPLogstashHandler(logging.Handler):
    """Python logging handler for Logstash. Sends events over TCP.
    :param url: Logstash url.
    :param message_type: The type of the message (default logstash).
    :param fqdn; Indicates whether to show fully qualified domain name or not (default False).
    :param version: version of logstash event schema (default is 0).
    :param tags: list of tags for a logger (default is None).
    """

    def __init__(
        self,
        url: str,
        message_type="logstash",
        tags=None,
        fqdn=False,
        version=0,
        username=None,
        password=None,
    ):
        super().__init__()
        self.url = url
        self.username = username
        self.password = password
        self.formatter = formatter.versions[version](message_type, tags, fqdn)

    def makePickle(self, record):
        return b'json='+str.encode(self.formatter.format(record))

    def emit(self, record):
        """
        Emit a record.

        Pickles the record and writes it to the socket in binary format.
        If there is an error with the socket, silently drop the packet.
        If there was a problem with the socket, re-establishes the
        socket.
        """
        try:
            s = self.makePickle(record)
            self.send(s)
        except Exception:
            self.handleError(record)

    def send(self, data: bytes):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if self.username and self.password:
            basic = b64encode(f"{self.username}:{self.password}".encode()).decode("utf-8")
            headers["authorization"] = f"Basic {basic}"

        httprequest = Request(self.url, data=data, headers=headers, method="POST")

        with urllib.request.urlopen(httprequest) as httpresponse:
            pass
            # status = httpresponse.status
            # body = httpresponse.read().decode(
            #     httpresponse.headers.get_content_charset("utf-8")
            # )
            # if status != 200:
            #     raise Exception(body)
