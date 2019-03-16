import requests
import json
import time
from web_api_handler import WebApiHandler


class TgBot:
    def __init__(self, token: str = None, USE_PROXY: bool = False):
        self.USE_PROXY = USE_PROXY
        self.token = token
        self.base_url = "https://api.telegram.org/bot{token}/".format(token=self.token)
        self.api = WebApiHandler

        self.user_actions = {
            '/start': self.start,
            '/create_note': self.create_note,
            '/get_notes': self.get_notes,
            '/get_note': self.get_note,
            '/delete_note': self.delete_note,
            '/edit_note': self.edit_note
        }

        self.bot_actions = {
            'get_updates': self.get_updates,
        }

        self.proxies = {}
        if USE_PROXY:
            self.proxies = {
                "http": "101.108.254.147:8080",
                "https": "101.108.254.147:8080",
            }

        self.timing = 3
        self.updates = None
        self.updates_length = 0
        self.text = None
        self.update_id = None
        self.chat_id = None
        self.action = None

        self.run()

    # bot base scrapping
    def run(self):
        self.updates = self.get_updates()
        print('ALL OKEY BOT STARTING WORK')
        self.updates_length = len(self.updates)
        while True:
            self.updates = self.get_updates()
            delta_length = len(self.updates) - self.updates_length
            if delta_length > 0:
                for i in range(self.updates_length, delta_length + self.updates_length):
                    #print(self.updates[i])
                    self.process(self.updates[i])
                self.updates_length += delta_length
            time.sleep(self.timing)

    def get_updates(self):
        return self.dict(requests.get(self.base_url+'getUpdates', proxies=self.proxies))

    def dict(self, request):
        returned = json.loads(request.text)
        if returned['ok']:
            return returned['result']
        return returned

    def process(self, update):
        self.update_id = update['update_id']
        messages = update['message']
        self.chat_id = update['message']['chat']['id']
        self.text: list = messages['text'].split(' ')
        self.action = self.text[0]
        self.text.pop(0)
        self.text = ' '.join(self.text)
        print(self.action, self.text)
        if self.action in self.user_actions:
            self.user_actions[self.action]()

    # bot actions methods
    def send_msg(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        requests.post(self.base_url + method, params, proxies=self.proxies)

    # user actions methods
    def start(self):
        self.send_msg(self.chat_id, 'welcome!')

    def create_note(self):
        self.api.post_note({'text': self.text})
        self.send_msg(self.chat_id, 'add note success!')

    def edit_note(self):
        pass

    def delete_note(self):
        pass

    def get_notes(self):
        self.send_msg(self.chat_id, str(self.api.get_note()))

    def get_note(self):
        self.send_msg(self.chat_id, str(self.api.get_note(self.text)))
