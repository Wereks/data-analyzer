from collections import defaultdict, Counter
from typing import Union

import numpy as np
from scipy.spatial import KDTree

from .classes import Post, User
from .api import DB

def _check_unique_id(objects: list[Union[User, Post]]) -> bool:
    """Checks if users or posts have unique id"""
    counter = Counter(object_.id for object_ in objects)
    non_unique = [(id_, count) for (id_, count) in counter.items() if count > 1]
    
    if non_unique:
        print(f'Found nonunique ids {non_unique}')
        return False

    return True

def objectify(objects: list[dict], class_: Union[Post, User]) -> list[Union[Post, User]]:
    """Returns a new list with dicts changed to instances of class_"""
    converted = [x if isinstance(x, class_) else class_(**x) for x in objects]

    return converted

def count(users: list[Union[dict, User]], posts: list[Union[dict, Post]]) -> list[str]:
    """Returns a list of strings which says how many posts an user wrote"""
    def _count(users: list[User], posts: list[Post]):
        counter = Counter(post.userId for post in posts)
        result = [(user.name, counter.get(user.id, 0)) for user in users]

        return [f'{user_name} napisał(a) {count} postów' for (user_name, count) in result]

    users = objectify(users, User)
    posts = objectify(posts, Post)
    if not _check_unique_id(users):
        raise ValueError("Users dont have unique ids")
    return _count(users, posts)

def non_unique(posts:  list[Union[dict, Post]]) -> list[str]:
    """Returns all the titles which are duplicates"""
    def _non_unique(posts: list[Post]):
        counter = Counter(post.title for post in posts)
        non_unique = [title for (title, count) in counter.items() if count > 1]

        return non_unique
    
    posts = objectify(posts, Post)
    if not _check_unique_id(posts):
        raise ValueError("Posts dont have unique ids")
    return _non_unique(posts)

def closests_ones(users : list[Union[dict, User]]) -> dict[str, str]:
    """Returns dict which maps user id to set of other user ids which live the closest"""
    def _closests_ones(users: list[User]):
        locations = defaultdict(set) 
        for user in users:
            locations[user.geo()].add(user.id)

        points = np.array(list(locations.keys()))
        tree = KDTree(points)

        result = {}
        for (geo, users_id) in locations.items():
            closest_point = geo
            if len(users_id) == 1:
                closest_point = tuple(points[tree.query(geo, k=2, workers=-1)[1][1]])

            for user_id in users_id:
                result[user_id] = set(idx for idx in locations[closest_point] if idx != user_id)

        return result

    users = objectify(users, User)
    
    if not _check_unique_id(users):
        raise ValueError("Users dont have unique ids")
    if len(users) <= 1:
        raise ValueError("Only 1 (or less) user exists, cant find closest one")

    return _closests_ones(users)