import logging

from src.exceptions.permissions import PermissionsExceptions
from src.modules.roles.config.permissions import Permissions
from src.modules.roles.service import RoleService, RolePermissionsService
from src.services.http import BaseResource
from src.services.http.auth_utils import auth_required
from src.services.http.errors import InternalServerError


class RolesResource(BaseResource):
    def __init__(self):
        self.service = RoleService()
        self.permissions = Permissions.index

    @auth_required()
    def get(self):
        try:
            self.apply_permissions()
            return self.service.find()
        except PermissionsExceptions as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    @auth_required()
    def post(self):
        try:
            self.apply_permissions()
            return self.service.create()
        except PermissionsExceptions as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()


class RolesOneResource(BaseResource):
    def __init__(self):
        self.service = RoleService()
        self.permissions = Permissions.self

    @auth_required()
    def get(self, model_id):
        try:
            self.apply_permissions()
            return self.service.find_one(model_id)
        except PermissionsExceptions as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    @auth_required()
    def patch(self, model_id):
        try:
            self.apply_permissions()
            return self.service.edit(model_id)
        except PermissionsExceptions as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    @auth_required()
    def delete(self, model_id):
        try:
            self.apply_permissions()
            return self.service.delete(model_id)
        except PermissionsExceptions as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()


class RolePermissionsResource(BaseResource):
    def __init__(self):
        self.service = RolePermissionsService()
        self.permissions = Permissions.permissions

    @auth_required()
    def get(self, model_id):
        try:
            self.apply_permissions()
            return self.service.get_permissions(model_id)
        except PermissionsExceptions as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    @auth_required()
    def put(self, model_id):
        try:
            self.apply_permissions()
            return self.service.update_permissions(model_id)
        except PermissionsExceptions as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()


class RolesListResource(BaseResource):
    def __init__(self):
        self.service = RoleService()
        self.permissions = Permissions.list

    @auth_required()
    def get(self):
        try:
            self.apply_permissions()
            return self.service.get_list()
        except PermissionsExceptions as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()
   