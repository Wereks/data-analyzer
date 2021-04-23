Module which lets you retrieve data of users and posts from  jsonplaceholder.typicode.com. 
Functions which lets you count number of posts made by an user,  pair the closests users by their geolocations and count the nonunique number of post titles.
The module also provides dataclasses in which you can store the dictionaries representing user/address/geolocation points and post in an object.

To use the module you need to:
**Before you start, if you're a windows user, make sure your environment in which python is installed, supports scipy**
1. Install pipenv, with the command `pip install pipenv`
2. Install all the dependencies (and the setup.py), with the  command `pipenv install`
3. Activate the pipenv shell in the root folder, `pipenv shell`
4. Run the example script with `py example.py` or run the tests with `pytest tests/` to check the coverage use `pytest --cov=main tests/`

An example code on how to use the module can be found in **example.py**
```python
from main import *

def change_ids_to_names(users):
    """Changes the usual format of closests to use names instead of ids"""
    users_objects = objectify(users, User)
    match_id_name = {user.id: user.name for user in users_objects}
    closests_with_names = []
    for id_, closests_id in closests.items():
 	    closests_list = [match_id_name[id_] for id_ in closests_id]
 	    closests_with_names.append((match_id_name[id_], closests_list))
	
    return closests_with_names

if __name__ == "__main__":
    db = DB()
    users = db.users()
    posts = db.posts()

    print(count(users, posts))
    print(non_unique(posts))
    closests = closests_ones(users)
    print(closests)
    print(change_ids_to_names(users))
```

