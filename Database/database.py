from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator

# Connect to the Couchbase cluster
cluster = Cluster('couchbase://localhost')
authenticator = PasswordAuthenticator('username', 'password')
cluster.authenticate(authenticator)

# Open a bucket
bucket = cluster.open_bucket('bucket_name')
