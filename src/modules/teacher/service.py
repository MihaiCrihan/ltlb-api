from flask import request
from flask import jsonify
from sqlalchemy import exc
import logging

from src.app import db
from src.modules.teacher.models import Teacher
from src.modules.teacher.repository import TeacherRepository
from src.modules.users.repository import UserRepository
from src.modules.users.models import User, UserRole
from src.modules.roles.models import Role
from src.modules.teacher.serializer import CreateTeacherSerializer
from datetime import datetime as dt

from src.services.http.errors import Success, UnprocessableEntity, InternalServerError, NotFound


class TeacherService:
    def __init__(self):
        self.repository = TeacherRepository()
        self.usersRepository = UserRepository()

    def find(self):
        headers = [
            {"value": "id", "text": "ID"},
            {"value": "first_name", "text": 'first name'},
            {"value": "last_name", "text": 'Last name'},
            {"value": "address", "text": 'Address'},
            {"value": "user_name", "text": 'User name'}
        ]

        params = request.args

        items = self.repository \
            .paginate(int(params.get('page', 1)), per_page=int(params.get('per_page', 20)))

        resp = {
            "items": [
                {
                    "first_name": item.first_name,
                    "last_name": item.last_name,
                    "address": item.address,
                    "user_name": item.user.name if item.user else '',
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
            )

            self.repository.create(model)
            db.session.commit()

            user = User()
            user.name = f"{data['first_name']} {data['last_name']}",
            user.email = data['email']
            user.confirmed_at = dt.utcnow().isoformat()
            user.is_active = True
            user.password = user.hash_password(data['password'])
            db.session.add(user)
            db.session.commit()

            guest_id = Role.query.filter_by(alias='guest').first()

            # user_role = UserRole(
            #     role_id=guest_id,
            #     user_id=user.id
            # )

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
                "address": model.address,
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
