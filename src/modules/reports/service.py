import logging
from flask import request
from sqlalchemy import func
from src.modules.teacher.models import TeacherCourse, Teacher
from src.modules.teacher.models import TeacherPositions
from src.services.http.errors import InternalServerError


class ReportService:
    def get_between_dates(self):
        try:
            params = request.args

            teachers = Teacher.query.with_entities(Teacher.id, Teacher.first_name, Teacher.last_name).all()
            response = []

            for teacher in teachers:
                courses = self.get_teacher_courses(teacher.id, end_date=params['end_date'],
                                                   start_date=params['start_date'])
                positions = self.get_teacher_positions(teacher.id)
                if len(courses):
                    response.append({
                        "teacher": {
                            "first_name": teacher.first_name,
                            "last_name": teacher.last_name
                        },
                        "courses": courses,
                        "positions": positions
                    })
            return response
        except Exception as e:
            logging.error(e)
            raise Exception(e)

    def get_between_dates_for_teacher(self, teacher_id):
        try:
            params = request.args
            teacher = Teacher.query.get(teacher_id)

            courses = self.get_teacher_courses(teacher_id, end_date=params['end_date'], start_date=params['start_date'])
            positions = self.get_teacher_positions(teacher_id)
            return {
                "teacher": {
                    "first_name": teacher.first_name,
                    "last_name": teacher.last_name
                },
                "courses": courses,
                "positions": positions
            }
        except Exception as e:
            logging.error(e)
            raise Exception(e)

    @staticmethod
    def get_teacher_courses(teacher_id, start_date=None, end_date=None):
        query = TeacherCourse.query.filter(TeacherCourse.teacher_id == teacher_id)
        if start_date:
            query = query.filter(func.date(TeacherCourse.created_at) >= start_date)

        if end_date:
            query = query.filter(func.date(TeacherCourse.created_at) <= end_date)

        return [{
            "id": item.id,
            "dates": item.dates,
            "credits": item.credits,
            "name": item.name,
            "description": item.description,
        } for item in query.all()]

    @staticmethod
    def get_teacher_positions(teacher_id):
        positions = TeacherPositions.query.filter_by(teacher_id=teacher_id).all()
        return [{
            "id": item.id,
            "position_id": item.position_id,
            "degree_id": item.degree_id,
            "work_experience": item.work_experience,
        } for item in positions]

