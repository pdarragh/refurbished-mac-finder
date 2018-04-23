from twilio.rest import Client as TwilioClient

class Notifier:
    def __init__(self, account_sid: str, auth_token: str, send_from: str):
        self._client = TwilioClient(account_sid, auth_token)
        self.send_from = send_from

    def send_message(self, message: str, send_to: str):
        self._client.messages.create(to=send_to, from_=self.send_from, body=message)
