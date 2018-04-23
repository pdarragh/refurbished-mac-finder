from twilio.rest import Client as TwilioClient

class Client:
    def __init__(self, account_sid: str, auth_token: str, send_from: str, send_to: str):
        self._client = TwilioClient(account_sid, auth_token)
        self.send_from = send_from
        self.send_to = send_to

    def send_message(self, message: str):
        self._client.messages.create(to=self.send_to, from_=self.send_from, body=message)
