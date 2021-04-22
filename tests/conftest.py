import json

import pytest

@pytest.fixture(scope="package")
def local_users():
    def _local_users(name):
        with open(f'.\\tests\\data\\{name}\\users.json') as f:
            return json.load(f)
    return _local_users

@pytest.fixture(scope="package")
def local_posts():
    def _local_posts(name):
        with open(f'.\\tests\\data\\{name}\\posts.json') as f:
            return json.load(f)
    return _local_posts