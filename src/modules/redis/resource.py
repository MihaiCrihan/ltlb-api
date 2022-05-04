import logging
from .service import RedisService
from src.services.http import BaseResource
from src.services.http.auth_utils import auth_required
from src.services.http.errors import InternalServerError


class RedisResource(BaseResource):
    def __init__(self):
        self.service = RedisService()

    @auth_required()
    def delete(self):
        try:
            return self.service.delete_all()
        except Exception as e:
            logging.error(e)
            return InternalServerError()
