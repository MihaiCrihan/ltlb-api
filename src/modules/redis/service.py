from src.services.redis import redis_service


class RedisService:
    def __init__(self):
        self.redis_service = redis_service

    def delete_all(self):
        return self.redis_service.delete_all()
