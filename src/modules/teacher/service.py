from flask import request
from flask import jsonify
from sqlalchemy import exc
import logging

from src.app import db
from src.modules.teacher.models import Teacher
from src.modules.teacher.repository import TeacherRepository
from src.modules.teacher.serializer import CreateTeacherSerializer

from src.services.http.errors import Success, UnprocessableEntity, InternalServerError, NotFound


class TeacherService:
    def __init__(self):
        self.repository = TeacherRepository()

    def find(self):
        headers = [
            {"value": "id", "text": "ID"},
            {"value": "first_name", "text": 'first name'},
            {"value": "last_name", "text": 'Last name'},
            {"value": "user_id", "text": 'User ID'},
            {"value": "positions", "text": 'positions'},
        ]

        params = request.args

        page = int(params.get('page', 1))
        page_size = int(params.get('page_size', 20))

        items = self.repository.paginate(page, per_page=page_size)

        resp = {
            "items": [
                {
                    "first_name": item.first_name,
                    "last_name": item.last_name,
                    "positions": item.positions,
                    "user_id": item.user_id,
                    "id": item.id,
                } for item in items.items],
            "pages": items.pages,
            "total": items.total,
            "headers": headers
        }

        return jsonify(resp)

    def create(self):
        try:
            data = request.json
            serializer = CreateTeacherSerializer(data)

            if not serializer.is_valid():
                return UnprocessableEntity(errors=serializer.errors)

            model = Teacher(
                first_name=data['first_name'],
                last_name=data['last_name'],
                user_id=data['user_id']
            )
            self.repository.create(model)
            db.session.commit()
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
                return NotFound(message='Teacher not found')

            return {
                "first_name": model.first_name,
                "last_name": model.last_name,
                "user_id": model.user_id,
                "id": model.id
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
            return Success()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return InternalServerError()

    def get_list(self):
        try:
            return self.repository.list()
        except Exception as e:
            logging.error(e)
            return InternalServerError()
