import inspect
import logging
import socket
import traceback
from datetime import datetime

try:
    import simplejson as json
except ImportError:
    import json


class LogstashFormatterBase(logging.Formatter):
    # The list contains all the attributes listed in
    # http://docs.python.org/library/logging.html#logrecord-attributes
    skip_list = {
        "args",
        "asctime",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "id",
        "levelname",
        "levelno",
        "lineno",
        "module",
        "msecs",
        "message",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "thread",
        "threadName",
        "extra",
    }

    easy_types = (str, bool, float, int, type(None))

    def __init__(self, message_type="Logstash", tags=None, fqdn=False):
        self.message_type = message_type
        self.tags = tags if tags is not None else []

        if fqdn:
            self.host = socket.getfqdn()
        else:
            self.host = socket.gethostname()

    def simplify(self, value):
        if isinstance(value, self.easy_types):
            return value
        elif isinstance(value, (list, tuple, set)):
            return type(value)(self.simplify(i) for i in value)
        elif isinstance(value, dict):
            return {self.simplify(k): self.simplify(v) for k, v in value.items()}
        else:
            return repr(value)

    def get_extra_fields(self, record):
        fields = {}

        for key, value in record.__dict__.items():
            if key not in self.skip_list:
                fields[key] = self.simplify(value)

        frame = self.get_frame(record)
        if frame:
            cls = self.get_class(frame)
            if cls:
                fields["class_name"] = cls.__module__ + "." + cls.__name__

        return fields

    @staticmethod
    def get_frame(record: logging.LogRecord):
        frame = inspect.currentframe()
        while frame:
            frame = frame.f_back
            frameinfo = inspect.getframeinfo(frame)
            if frameinfo.filename == record.pathname:
                return frame

    @staticmethod
    def get_class(frame):
        if "self" in frame.f_locals:
            return type(frame.f_locals["self"])
        elif "cls" in frame.f_locals:
            return frame.f_locals["cls"]

    def get_debug_fields(self, record):
        fields = {
            "stack_trace": self.format_exception(record.exc_info),
            "lineno": record.lineno,
            "process": record.process,
            "thread_name": record.threadName,
        }

        # funcName was added in 2.5
        if not getattr(record, "funcName", None):
            fields["funcName"] = record.funcName

        # processName was added in 2.6
        if not getattr(record, "processName", None):
            fields["processName"] = record.processName

        return fields

    @classmethod
    def format_source(cls, message_type, host, path):
        return "%s://%s/%s" % (message_type, host, path)

    @classmethod
    def format_timestamp(cls, time):
        tstamp = datetime.utcfromtimestamp(time)
        return "%s.%03dZ" % (
            tstamp.strftime("%Y-%m-%dT%H:%M:%S"),
            tstamp.microsecond / 1000,
        )

    @classmethod
    def format_exception(cls, exc_info):
        return "".join(traceback.format_exception(*exc_info)) if exc_info else ""

    @classmethod
    def serialize(cls, message):
        return json.dumps(message)

    def get_message(self, record: logging.LogRecord) -> dict:
        raise NotImplementedError()

    def format(self, record: logging.LogRecord) -> str:
        message = self.get_message(record)
        return self.serialize(message)


class LogstashFormatterVersion0(LogstashFormatterBase):
    def get_message(self, record):
        # Create message dict
        message = {
            "@timestamp": self.format_timestamp(record.created),
            "@message": record.getMessage(),
            "@source": self.format_source(
                self.message_type, self.host, record.pathname
            ),
            "@source_host": self.host,
            "@source_path": record.pathname,
            "@tags": self.tags,
            "@type": self.message_type,
            "@fields": {
                "levelname": record.levelname,
                "logger": record.name,
            },
        }

        # Add extra fields
        message["@fields"].update(self.get_extra_fields(record))

        # If exception, add debug info
        if record.exc_info:
            message["@fields"].update(self.get_debug_fields(record))

        return message


class LogstashFormatterVersion1(LogstashFormatterBase):
    def get_message(self, record):
        # Create message dict
        message = {
            "@timestamp": self.format_timestamp(record.created),
            "message": record.getMessage(),
            "host": self.host,
            "path": record.pathname,
            "tags": self.tags,
            "type": self.message_type,
            # Extra Fields
            "level": record.levelname,
            "logger_name": record.name,
        }

        # Add extra fields
        message.update(self.get_extra_fields(record))

        # If exception, add debug info
        if record.exc_info:
            message.update(self.get_debug_fields(record))

        return message


versions = {0: LogstashFormatterVersion0, 1: LogstashFormatterVersion1}
