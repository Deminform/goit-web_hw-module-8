import os

from mongoengine import connect
import configparser
import redis

config_file_path = os.path.join(os.path.dirname(__file__), 'config.ini')

config = configparser.ConfigParser()
config.read(config_file_path)

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

rd_host = config.get('RD', 'rd_host')
rd_port = config.get('RD', 'rd_port')

# connect to cluster on AtlasDB with connection string
connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)

# connect to Redis
client = redis.StrictRedis(host=rd_host, port=rd_port, password=None)
