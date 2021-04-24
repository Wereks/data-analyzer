from copy import deepcopy
import json
from functools import partialmethod

import requests

class DB:
    def __init__(self):
        self.headers = {'User-Agent': 'bot-github.com/Wereks/data-analyzer'}
        self._users = None
        self._posts = None

    def _get(self, name, local=False, refresh=False):
        """Gets data from the {name} attribute
        :param name: name of the attribute to get
        :param local: (optional) if ``True``, the data will come from the local storage containing data from last successful response Defaults: ``False``
        :param refresh: (optional) if ``True``, the data will be downloaded from the external API (ignored if local is ``True``) Defaults: ``False``
        :rtype list
        """
        a_name = f'_{name}'
        if local:
            setattr(self, a_name, self._load(name))
        elif refresh or getattr(self, a_name) is None:
            response = requests.get(f'https://jsonplaceholder.typicode.com/{name}', headers=self.headers)
            json_ = response.json()
            setattr(self, a_name, json_)
            self._save(name, json_)

        return deepcopy(getattr(self, a_name))

    def users(self, local=False, refresh=False):
        return self._get('users', local, refresh)

    def posts(self, local=False, refresh=False):
        return self._get('posts', local, refresh)

    def _load(self, name):
        with open(f'./main/db/{name}.json') as f:
            return json.load(f)

    def _save(self, name, json_):
        with open(f'./main/db/{name}.json', mode='w') as f:
            return json.dump(json_, f)