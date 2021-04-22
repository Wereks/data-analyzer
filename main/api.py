from copy import deepcopy
import json

import requests

class DB:
    def __init__(self):
        self.headers = {'User-Agent': 'bot-github.com/Wereks/'}
        self._users = None
        self._posts = None

    def users(self, refresh=False):
        if refresh or self._users is None:
            self._users = requests.get("https://jsonplaceholder.typicode.com/users").json()

        return deepcopy(self._users)

    def posts(self, refresh=False):
        if refresh or self._posts is None:
            self._posts = requests.get("https://jsonplaceholder.typicode.com/posts").json()

        return deepcopy(self._posts)    