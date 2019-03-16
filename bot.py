import json
import requests
import time
from web_api_handler import WebApiHandler


class Bot:
    base_url = "https://api.telegram.org/bot{token}/"
    use_proxy = False

    def __init__(self, token=None, use_proxy=False):
        self.base_url = self.base_url.format(token=token)
        self.api = WebApiHandler
        self.movies_dict = {
            '/hello': self.hello,
            '/check': self.check_notes
        }
        self.proxies = None
        self.notes = []
        if use_proxy:
            self.proxies = {
                "http": "77.65.113.202:8080",
                "https": "77.65.113.202:8080",
            }
            self.use_proxy = True
        self.updates = self.getUpdates()
        self.updates_length = len(self.updates)
        while True:
            self.updates = self.getUpdates()
            delta_lenght = len(self.updates) - self.updates_length
            if delta_lenght > 0:
                for i in range(self.updates_length, delta_lenght + self.updates_length):
                    self.check_update(self.updates[i])
                self.updates_length += delta_lenght
            time.sleep(1)

    def getUpdates(self):
        return self.json_to_dict(requests.get(self.base_url + 'getUpdates', proxies=self.proxies))

    def json_to_dict(self, request):
        returned = json.loads(request.text)
        if returned['ok']:
            return returned['result']
        return returned

    def sendMessage(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        requests.post(self.base_url + method, params, proxies=self.proxies)

    def check_update(self, update):
        update_id = update['update_id']
        messages = update['message']
        move = messages['text']
        if move in self.movies_dict:
            self.movies_dict[move](messages)
        else:
            self.api.post_note(payload={'text': move})

    def hello(self, message):
        self.sendMessage(message['chat']['id'], 'hello!')

    def check_notes(self, message):
        self.sendMessage(message['chat']['id'], str(self.api.get_note()))
