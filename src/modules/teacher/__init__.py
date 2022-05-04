from src.app import api
from src.modules.teacher.resource import TeacherResource
from src.modules.teacher.resource import TeacherListResource
from src.modules.teacher.resource import TeacherOneResource
from src.modules.teacher.resource import TeacherCoursesResource
from .models import Teacher

resource = '/teachers'

api.add_resource(TeacherResource, resource)
api.add_resource(TeacherOneResource, f'{resource}/<model_id>')
api.add_resource(TeacherListResource, f'{resource}/list')
api.add_resource(TeacherCoursesResource, f'{resource}/courses/list')
