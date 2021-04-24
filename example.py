from main import *

def change_ids_to_names(closests, users):
    """Changes the usual format of closests to use names instead of ids"""
    users_objects = objectify(users, User)
    match_id_name = {user.id: user.name for user in users_objects}
    closests_with_names = []
    for id_, closests_id in closests.items():
        closests_list = [match_id_name[id_] for id_ in closests_id]
        closests_with_names.append((match_id_name[id_], closests_list))

    return closests_with_names

if __name__ == "__main__":
    db = DB()
    users = db.users()
    posts = db.posts()

    print(count(users, posts))
    print(non_unique(posts))

    closests = closests_ones(users)
    print(closests)
    print(change_ids_to_names(closests, users))