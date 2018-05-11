from couchbase.exceptions import KeyExistsError
from couchbase_server import Buckets
import ad_stuff


def __insert_author(username, name, phone=None, email=None):
    author_data = dict(username=username, name=name)
    if phone:
        author_data['phone'] = phone
    if email:
        author_data['email'] = email
    try:
        Buckets.author_bucket.insert(username, author_data)
        print("Author inserted!")
    except KeyExistsError:
        print("Username '{}' already exists".format(username))


def insert_author_main():
    username = input("Username:\t")
    name = input("Name:\t")
    phone = input("Phone:\t")
    email = input("Email:\t")
    __insert_author(username, name, phone, email)


def get_author(username):
    return Buckets.author_bucket.get(username, quiet=True).value


def delete_author(username):
    ads_to_delete = list(ad['date'] for ad in ad_stuff.get_ads_for_author(username))
    ad_stuff.delete_ads(*ads_to_delete)
    Buckets.author_bucket.remove(username)
    print("Author deleted")


def get_all_authors():
    query = "SELECT * from ad_authors WHERE username"
    return list(entry['ad_authors'] for entry in Buckets.author_bucket.n1ql_query(query))
