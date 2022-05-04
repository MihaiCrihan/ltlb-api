from src.app import api
from .resource import RedisResource

resource = '/redis/delete_all'

api.add_resource(RedisResource, resource)
