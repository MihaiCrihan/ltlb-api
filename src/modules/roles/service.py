from flask import request
from flask import jsonify
from sqlalchemy import exc
import logging

from src.app import db
from src.modules.roles.models import Role, RolePermissions
from src.modules.roles.repository import RoleRepository, RolePermissionsRepository
from src.modules.roles.serializer import CreateRoleSerializer

from src.services.http.errors import Success, UnprocessableEntity, InternalServerError, NotFound


class RoleService:
    def __init__(self):
        self.repository = RoleRepository()
        self.rolePermission = RolePermissionsRepository()

    def find(self):
        headers = [
            {"value": "id", "text": "ID"},
            {"value": "name", "text": 'Name'},
            {"value": "alias", "text": "Alias"}
        ]

        params = request.args

        items = self.repository \
            .paginate(int(params.get('page', 1)), per_page=int(params.get('per_page', 20)))

        resp = {
            "items": [
                {
                    "name": item.name,
                    "alias": item.alias,
                    "id": item.id
                } for item in items.items],
            "pages": items.pages,
            "total": items.total,
            "headers": headers
        }

        return jsonify(resp)

    def create(self):
        try:
            data = request.json
            serializer = CreateRoleSerializer(data)

            if not serializer.is_valid():
                return UnprocessableEntity(errors=serializer.errors)

            user = Role(
                name=data['name'],
                alias=data['alias']
            )
            self.repository.create(user)
            db.session.commit()
            return Success()
        except exc.IntegrityError as e:
            return UnprocessableEntity(message=f"{e.orig.diag.message_detail}")
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return InternalServerError()

    def find_one(self, user_id):
        try:
            user = self.repository.find_one_or_fail(user_id)

            if not user:
                return NotFound(message='Role not found')

            return {
                "name": user.name,
                "alias": user.alias,
                "id": user.id
            }
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    def edit(self, user_id):
        try:
            data = request.json
            user = self.repository.get(user_id)

            if not user:
                return NotFound()

            self.repository.update(user, data)
            db.session.commit()
            return Success()
        except exc.IntegrityError as e:
            logging.error(e)
            return UnprocessableEntity(message=f"{e.orig.diag.message_detail}")
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    def delete(self, user_id):
        try:
            user = self.repository.get(user_id)

            if not user:
                return NotFound()

            self.repository.remove(user)
            db.session.commit()
            return Success()
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    def get_list(self):
        try:
            return self.repository.list()
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    def update_permissions(self, model_id):
        try:
            data = request.json
            old_permissions = self.rolePermission.get_permissions(model_id)

            for item in old_permissions:
                if item not in data['permissions']:
                    self.rolePermission.remove(item)

            for item in data['permissions']:
                if not self.rolePermission.get(item):
                    perm = RolePermissions()
                    perm.role_id = model_id
                    perm.permission_id = item
                    self.rolePermission.create(perm)

            db.session.commit()
            return Success()
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    def get_permissions(self, model_id):
        try:
            return self.rolePermission.get_permissions(model_id)
        except Exception as e:
            logging.error(e)
            return InternalServerError()