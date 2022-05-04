from flask import request
from flask import jsonify
from sqlalchemy import exc
import logging

from src.app import db
from .models import Position
from .repository import PositionRepository
from .serializer import CreatePositionSerializer

from src.services.http.errors import Success
from src.services.http.errors import UnprocessableEntity
from src.services.http.errors import InternalServerError
from src.services.http.errors import NotFound

from src.services.redis import redis_service, RedisKeys

from src.services.localization import Locales


class PositionService:
    def __init__(self):
        self.repository = PositionRepository()
        self.t = Locales()

    def find(self):
        headers = ["id", "name"]

        params = request.args

        items = self.repository \
            .paginate(int(params.get('page', 1)), per_page=int(params.get('per_page', 20)))

        resp = {
            "items": [
                {
                    "id": item.id,
                    "name": item.name
                } for item in items.items],
            "pages": items.pages,
            "total": items.total,
            "headers": [{
                "value": item,
                "text": self.t.translate(f'positions.fields.{item}')
            } for item in headers]
        }

        return jsonify(resp)

    def create(self):
        try:
            data = request.json or request.form

            serializer = CreatePositionSerializer(data=data)

            if not serializer.is_valid():
                return UnprocessableEntity(errors=serializer.errors)

            model = Position(
                name=data['name'],
            )
            self.repository.create(model)
            db.session.commit()

            redis_service.set(RedisKeys.positions_list, self.repository.list())
            return Success()
        except exc.IntegrityError as e:
            return UnprocessableEntity(message=f"{e.orig.diag.message_detail}")
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return InternalServerError()

    def find_one(self, model_id):
        try:
            model = self.repository.find_one_or_fail(model_id)

            if not model:
                return NotFound(message='Position not found')

            return {
                    "id": model.id,
                    "name": model.name
                }
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    def edit(self, user_id):
        try:
            data = request.json
            model = self.repository.get(user_id)

            if not model:
                return NotFound()

            self.repository.update(model, data)
            db.session.commit()

            redis_service.set(RedisKeys.positions_list, self.repository.list())
            return Success()
        except exc.IntegrityError as e:
            db.session.rollback()
            logging.error(e)
            return UnprocessableEntity(message=f"{e.orig.diag.message_detail}")
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return InternalServerError()

    def delete(self, model_id):
        try:
            model = self.repository.get(model_id)

            if not model:
                return NotFound()

            self.repository.remove(model)
            db.session.commit()
            redis_service.set(RedisKeys.positions_list, self.repository.list())
            return Success()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return InternalServerError()

    def get_list(self):
        try:
            if redis_service.get(RedisKeys.positions_list):
                return redis_service.get(RedisKeys.positions_list)

            items = self.repository.list()
            redis_service.set(RedisKeys.positions_list, items)
            return items
        except Exception as e:
            logging.error(e)
            return InternalServerError()
