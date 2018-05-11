from couchbase.cluster import Cluster, PasswordAuthenticator
from couchbase.exceptions import NotFoundError, KeyExistsError
from couchbase.admin import Admin


SERVER_IP = "137.112.89.94"

SERVER_IP = "137.112.89.94"

cluster = Cluster('couchbase://{}:8091'.format(SERVER_IP))
__authenticator = PasswordAuthenticator('admin', 'An3WeeWa')
cluster.authenticate(__authenticator)

adm = Admin('admin', 'An3WeeWa', host=SERVER_IP, port=8091)


class Buckets(object):
    ad_bucket = cluster.open_bucket('ad_listings')
    author_bucket = cluster.open_bucket('ad_authors')

    __all = [ad_bucket, author_bucket]
    _timeout = 5.000

    for bucket in __all:
        bucket.timeout = _timeout

    def __iter__(self):
        for bucket in Buckets.__all:
            yield bucket


"""
CREATE INDEX username ON `ad_authors`(username)
CREATE INDEX author ON `ad_listings`(author)
CREATE INDEX `price` ON `ad_listings`(`price`)
CREATE INDEX timestamp ON `ad_listings`(date)
"""
