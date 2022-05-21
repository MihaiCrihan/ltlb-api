import logging
from src.exceptions.permissions import PermissionsExceptions
from .config.permissions import Permissions
from .service import ReportService
from src.services.http import BaseResource
from src.services.http.auth_utils import auth_required
from src.services.http.errors import InternalServerError


class ReportResource(BaseResource):
    def __init__(self):
        self.service = ReportService()
        self.permissions = Permissions.self

    @auth_required()
    def get(self):
        try:
            return self.service.get_between_dates()
        except PermissionsExceptions as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()


class ReportOneResource(BaseResource):
    def __init__(self):
        self.service = ReportService()

    @auth_required()
    def get(self, user_id):
        try:
            return self.service.get_between_dates_for_teacher(user_id)
        except Exception as e:
            logging.error(e)
            return InternalServerError()
