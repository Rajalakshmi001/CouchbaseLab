from random import randint
import datetime
from couchbase.exceptions import KeyExistsError
from couchbase_server import Buckets
from ad_stuff import insert_ad_main, get_all_ads, get_ads_for_author, ads_by_price, ads_by_date, edit_ad_main, \
    filter_by_price_main
from author_stuff import insert_author_main, get_author, delete_author, get_all_authors

options = [
    "Insert a new ad",
    "Add a new author",
    "Delete a author and all of their ads",
    "Get all ads by a certain author",
    "Sort ads by price",
    "Sort ads chronologically",
    "Get author details",
    "Get all ads",
    "Get all authors",
    "Edit an ad",
    "Filter with a maximum price"
]


def print_list(ls):
    for i, item in enumerate(ls):
        print("{}.".format(i), item)


def main():
    print()
    print("=" * 50)
    for i, opt in enumerate(options):
        print("{}.\t{}".format(i + 1, opt))

    try:
        option = int(input("Enter a number to choose an option:\t"))
        assert 1 <= option <= len(options)
    except:
        print("Invalid input")
        return

    print(option, '-', options[option - 1])
    if option == 1:
        # insert new ad
        insert_ad_main()
    elif option == 2:
        # insert new author
        insert_author_main()
    elif option == 3:
        # delete author and all of their ads
        delete_author(input("Username to delete:\t"))
    elif option == 4:
        # Get all ads by a author
        print_list(get_ads_for_author(input("Username:\t")))
    elif option == 5:
        # sort ads by price
        print_list(ads_by_price())
    elif option == 6:
        # sort ads by date
        print_list(ads_by_date())
    elif option == 7:
        # get author details
        print(">", get_author(input("Username:\t")) or "author not found")
    elif option == 8:
        print_list(get_all_ads())
    elif option == 9:
        print_list(get_all_authors())
    elif option == 10:
        edit_ad_main()
    elif option == 11:
        print_list(filter_by_price_main())


if __name__ == '__main__':
    while 1:
        try:
            main()
        except Exception as e:
            print(type(e), e)
