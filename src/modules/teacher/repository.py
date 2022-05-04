from src.app import db
from src.modules.teacher.models import Teacher
from src.modules.teacher.models import TeacherPositions
from src.modules.teacher.models import TeacherCourse


class TeacherRepository(Teacher):
    def find(self, **kwargs):
        return self.query.filter_by(**kwargs).all()

    def get(self, model_id):
        return self.query.get(model_id)

    def find_one(self, **kwargs):
        return self.query.filter_by(**kwargs).first()

    def find_one_or_fail(self, model_id):
        return self.query.get(model_id)

    @staticmethod
    def remove(model):
        db.session.delete(model)
        return True

    @staticmethod
    def create(model):
        db.session.add(model)
        return True

    def paginate(self, **kwargs):
        query = self.query
        page = kwargs.get('page', 1)
        page_size = kwargs.get('page_size', 20)

        filters = kwargs.get('filters', None)

        if filters is not None:
            for key in kwargs['filters']:
                if key == 'degree_id':
                    teachers_ids = [item.teacher_id for item in
                                    TeacherPositions.query.filter_by(degree_id=kwargs["filters"][key]).all()]
                    query = query.filter(Teacher.id.in_(teachers_ids))

                if key == 'course_id':
                    courses_ids = [item.id for item in
                                   TeacherCourse.query.filter_by(id=kwargs["filters"][key]).all()]
                    query = query.filter(Teacher.id.in_(courses_ids))

                elif key == 'first_name' and filters.get(key, None):
                    query = query.filter(Teacher.first_name.ilike(f'%{filters["first_name"]}%'))

                elif key == 'last_name' and filters.get(key, None):
                    query = query.filter(Teacher.last_name.ilike(f'%{filters["last_name"]}%'))

                elif hasattr(self, key):
                    query = query.filter(getattr(self, key) == kwargs["filters"][key])

        response = query.paginate(page=page, per_page=page_size, error_out=False)

        return {
            "items": response.items,
            "pages": response.pages,
            "total": response.total,
            "page_size": page_size,
            "page": page,
        }

    @staticmethod
    def update(model, data):
        for (key, value) in data.items():
            if hasattr(model, key):
                setattr(model, key, value)
        return model

    def list(self):
        return [
            {
                "id": item.id,
                "user_id": item.user_id,
                "first_name": item.first_name,
                "last_name": item.last_name,
                "email": item.user.email if item.user else ""
            } for item in self.query.all()]

    @staticmethod
    def get_courses():
        return [
            {
                "value": item.id,
                "text": item.name
            } for item in TeacherCourse.query.with_entities(TeacherCourse.id, TeacherCourse.name).all()]
