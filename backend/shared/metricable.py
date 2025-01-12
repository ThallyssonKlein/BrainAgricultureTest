#from datadog import initialize, statsd

class Metricable:
    def __init__(self, namespace: str):
        self.namespace = namespace

    class Metrics:
        def __init__(self, namespace: str):
            self.namespace = namespace

        def _format_key(self, key: str) -> str:
            return f"{self.namespace}.{key}"

        def increment(self, key: str, value: int = 1, tags: list = None):
            formatted_key = self._format_key(key)
            #statsd.increment(formatted_key, value, tags=tags)

        def decrement(self, key: str, value: int = 1, tags: list = None):
            formatted_key = self._format_key(key)
            #statsd.decrement(formatted_key, value, tags=tags)

        def histogram(self, key: str, value: float, tags: list = None):
            """Envia um valor para um histograma"""
            formatted_key = self._format_key(key)
            #statsd.histogram(formatted_key, value, tags=tags)

    def create_metrics(self):
        return self.Metrics(self.namespace)
