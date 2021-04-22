import json

import pytest

from main import *

@pytest.fixture(scope='module')
def db():
    return DB()

@pytest.fixture()
def users(db):
    return db.users()

@pytest.fixture()
def posts(db):
    return db.posts()

def test_users(users, local_users):
    assert json.dumps(users, sort_keys=True) == json.dumps(local_users('example'), sort_keys=True)

def test_posts(posts, local_posts):
    assert json.dumps(posts, sort_keys=True) == json.dumps(local_posts('example'), sort_keys=True)   

def test_count(users, posts):
    assert sorted(count(users, posts)) == ['Chelsey Dietrich napisał(a) 10 postów', 'Clementina DuBuque napisał(a) 10 postów', 'Clementine Bauch napisał(a) 10 postów', 'Ervin Howell napisał(a) 10 postów', 'Glenna Reichert napisał(a) 10 postów', 'Kurtis Weissnat napisał(a) 10 postów', 'Leanne Graham napisał(a) 10 postów', 'Mrs. Dennis Schulist napisał(a) 10 postów', 'Nicholas Runolfsdottir V napisał(a) 10 postów', 'Patricia Lebsack napisał(a) 10 postów']

def test_non_unique(posts):
    assert non_unique(posts) == []

def test_closests(users):
    assert closests_ones(users) == {1: {5}, 2: {3}, 3: {2}, 4: {9}, 5: {10}, 6: {1}, 7: {5}, 8: {4}, 9: {4}, 10: {5}}

def test_example(users, posts):
    test_count(users, posts)
    test_non_unique(posts)
    test_closests(users)

    closests = closests_ones(users)
    users_objects = objectify(users, User)
    match_id_name = {user.id: user.name for user in users_objects}
    closests_with_names = []
    for id_, closests_id in closests.items():
        closests_list = [match_id_name[id_] for id_ in closests_id]
        closests_with_names.append((match_id_name[id_], closests_list))

    assert sorted(closests_with_names) == sorted([('Leanne Graham', ['Chelsey Dietrich']), ('Ervin Howell', ['Clementine Bauch']), ('Clementine Bauch', ['Ervin Howell']), ('Patricia Lebsack', ['Glenna Reichert']), ('Chelsey Dietrich', ['Clementina DuBuque']), ('Mrs. Dennis Schulist', ['Leanne Graham']), ('Kurtis Weissnat', ['Chelsey Dietrich']), ('Nicholas Runolfsdottir V', ['Patricia Lebsack']), ('Glenna Reichert', ['Patricia Lebsack']), ('Clementina DuBuque', ['Chelsey Dietrich'])])

def test_renew_users(db):
    assert id(db._users) != id(users)
    db.users(refresh=True)
    assert id(users) != id(db._users)

def test_renew_posts(db):
    assert id(db._posts) != id(posts)
    db.posts(refresh=True)
    assert id(posts) != id(db._posts)
