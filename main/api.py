from copy import deepcopy

import requests

class DB:
    def __init__(self):
        self.headers = {'User-Agent': 'bot-github.com/Wereks/data-analyzer'}
        self._users = None
        self._posts = None

    def _get(self, url):
        return requests.get(url, headers=self.headers).json()

    def users(self, refresh=False):
        if refresh or self._users is None:
            self._users = self._get("https://jsonplaceholder.typicode.com/users")

        return deepcopy(self._users)

    def posts(self, refresh=False):
        if refresh or self._posts is None:
            self._posts = self._get("https://jsonplaceholder.typicode.com/posts")

        return deepcopy(self._posts)    