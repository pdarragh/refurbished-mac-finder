from twilio.rest import Client as TwilioClient

class Notifier:
    def __init__(self, account_sid: str, auth_token: str, send_from: str, no_notify: bool):
        self._client = None
        if not no_notify:
            self._client = TwilioClient(account_sid, auth_token)
        self.send_from = send_from

    def send_message(self, message: str, send_to: str):
        if self._client is not None:
            self._client.messages.create(to=send_to, from_=self.send_from, body=message)

