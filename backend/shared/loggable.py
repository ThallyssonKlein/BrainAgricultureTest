import datetime
import sys


class Loggable:
    def __init__(self, prefix: str):
        self.prefix = prefix
        self.log = self.Logger(prefix)

    class Logger:
        def __init__(self, prefix: str):
            self.prefix = prefix

        def _format_message(self, level: str, message: str, trace_id: str = None) -> str:
            timestamp = datetime.datetime.utcnow().isoformat()
            trace_part = f"[{trace_id}]" if trace_id else ""
            return f"{timestamp} {self.prefix} {level}: {trace_part} {message}"

        def info(self, message: str, trace_id: str = None):
            print(self._format_message('info', message, trace_id))

        def error(self, message: str, trace_id: str = None):
            print(self._format_message('error', message, trace_id), file=sys.stderr)
