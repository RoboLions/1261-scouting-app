from boto.s3.connection import S3Connection
import os

s3 = S3Connection(os.environ['MONGO_DB_URI'], os.environ['X_TBA_Auth_Key'], os.environ['PASSWORD'])

MONGO_DB_URI = os.environ.get('MONGO_DB_URI')
X_TBA_Auth_Key = os.environ.get('X_TBA_Auth_Key')
PASSWORD = os.environ.get('PASSWORD')