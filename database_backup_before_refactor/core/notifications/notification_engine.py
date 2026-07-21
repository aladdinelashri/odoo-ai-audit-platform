class NotificationEngine:

    def __init__(self):
        self.notifications = []


    def send(
        self,
        recipient,
        message,
        level="info"
    ):

        self.notifications.append({
            "recipient": recipient,
            "message": message,
            "level": level
        })


    def all(self):

        return self.notifications
