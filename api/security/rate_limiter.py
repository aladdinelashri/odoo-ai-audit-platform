from datetime import datetime, timedelta


class RateLimiter:

    def __init__(
        self,
        limit=100,
        window_minutes=60
    ):

        self.limit = limit
        self.window = timedelta(
            minutes=window_minutes
        )
        self.requests = {}


    def allow(
        self,
        client_id
    ):

        now = datetime.utcnow()

        history = self.requests.get(
            client_id,
            []
        )

        history = [
            timestamp
            for timestamp in history
            if now - timestamp < self.window
        ]

        if len(history) >= self.limit:
            self.requests[client_id] = history
            return False

        history.append(now)
        self.requests[client_id] = history

        return True
