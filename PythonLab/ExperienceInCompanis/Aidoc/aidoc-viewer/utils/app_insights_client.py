from applicationinsights import TelemetryClient


class AppInsightsClient:
    def __init__(self):
        self._client = None

    def init_app(self, key, max_queue_length=0):
        if not key or len(key) == 0:
            return

        self._client = TelemetryClient(key)
        self._client.channel.queue.max_queue_length = max_queue_length

    def track_metric(self, name, value, properties=None):
        if not self._client:
            return

        self._client.track_metric(name, value, properties=properties)


app_insights_client = AppInsightsClient()
