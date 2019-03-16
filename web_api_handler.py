import json
import requests


class WebApiHandler:
    base_url = 'http://restapi-licey2.herokuapp.com/api/v1/urls/'

    headers = {
        'content-type': "application/json",
        'authorization': "Basic YWRtaW46YWRtaW4=",
        'cache-control': "no-cache",
    }

    @classmethod
    def get_note(cls, id=None):
        if id is not None:
            return json.loads(requests.get(cls.base_url+str(id)).text)
        else:
            return json.loads(requests.get(cls.base_url).text)

    @classmethod
    def post_note(cls, payload):
        payload = cls.check_payload(payload)
        return requests.post(WebApiHandler.base_url, data=json.dumps(payload), headers=cls.headers)

    @classmethod
    def put_note(cls, id, payload):
        payload = cls.check_payload(payload)
        return requests.put(cls.base_url+str(id), data=json.dumps(payload), headers=cls.headers)

    @classmethod
    def delete_note(cls, id):
        requests.delete(cls.base_url + str(id), headers=cls.headers)

    @classmethod
    def check_payload(self, payload: dict):
        if ('url', 'text') in payload:
            return payload
        if 'url' not in payload:
                payload['url'] = ''
        elif 'text' not in payload:
                payload['text'] = ''
        return payload
