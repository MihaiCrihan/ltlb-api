from src.app import api
from .resource import ReportResource
from .resource import ReportOneResource

resource = '/reports'

api.add_resource(ReportResource, resource)
api.add_resource(ReportOneResource, f'{resource}/<int:user_id>')
