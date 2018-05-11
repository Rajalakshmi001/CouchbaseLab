import datetime
from couchbase.exceptions import KeyExistsError
from couchbase_server import Buckets
import author_stuff


def run_ad_query(query):
    """
    Executes a query that will result in everything being nested under
    'ad_listings' keys (a starred query) and returns the results.
    """
    results = list(entry['ad_listings'] for entry in Buckets.ad_bucket.n1ql_query(query))
    return results


def __insert_ad(ad_dict):
    if not ad_dict:
        print("No data specified")
        return False

    if not author_stuff.get_author(ad_dict['author']):
        print("Not a valid username")
        return False

    date = str(datetime.datetime.utcnow().isoformat())
    ad_dict['date'] = date

    try:
        Buckets.ad_bucket.insert(date, ad_dict)
        print("Ad inserted")
        return True
    except KeyExistsError:
        print("Someone else inserted an ad at the exact same time")
        return False
    except Exception as e:
        print("Failed to insert new ad:", type(e), e)
        return False


def prompt_for_ad():
    title = input("Input title for the ad: ")
    description = input("Input a description for the ad: ")
    author = input("Input the author's username: ")
    price = float(input("Input the price as a float: "))
    ad_dict = dict(title=title, description=description, author=author, price=price)
    for field in ad_dict:
        if ad_dict[field] is None:
            print("Must supply a {} for ads".format(field))
            return None
    return ad_dict


def insert_ad_main():
    ad = prompt_for_ad()
    __insert_ad(ad)


def get_all_ads():
    query = "SELECT * from ad_listings WHERE author"
    return run_ad_query(query)


def get_ads_for_author(username=None):
    username = username or input("Username: ")
    query = 'SELECT * from ad_listings WHERE author="{}"'.format(username)
    return run_ad_query(query)


def delete_ads(*timestamps):
    Buckets.ad_bucket.remove_multi(timestamps, quiet=True)
    print("Deleted", len(timestamps), "ads")


def ads_by_price():
    query = "SELECT * FROM ad_listings WHERE price OR NOT price ORDER BY PRICE"
    return run_ad_query(query)


def ads_by_date():
    query = "SELECT * FROM ad_listings WHERE date ORDER BY date"
    return run_ad_query(query)


def edit_ad_main():
    ads = get_ads_for_author()
    if not ads:
        print("That author has no ads")
        return False
    print("Ads by that author: ")
    for i, ad in enumerate(ads):
        print(i + 1, '-', ad)

    try:
        ad_to_edit = ads[int(input("Select an ad to edit: ")) - 1]
        print("\nEditing", ad_to_edit)
    except:
        print("Invalid selection")
        return False

    for field in ['title', 'description', 'price']:
        orig_value = ad_to_edit[field]
        ad_to_edit[field] = input("Enter a new {} ({}): ".format(field, orig_value)) or orig_value
    print()
    try:
        ad_to_edit['price'] = float(ad_to_edit['price'])
        assert ad_to_edit['price'] >= 0.0
    except:
        print("Invalid price:", ad_to_edit['price'])
        return False

    try:
        Buckets.ad_bucket.replace(ad_to_edit['date'], ad_to_edit)
        print("Ad updated")
        return True
    except Exception as e:
        print("Could not update ad:", type(e), e)
        return False


def filter_by_price_main():
    try:
        max_price = float(input("Insert max price to filter by:\t"))
    except:
        print("Invalid price input")
        return []

    query = "SELECT * FROM ad_listings WHERE price <= {} ORDER BY price".format(max_price)
    return run_ad_query(query)
