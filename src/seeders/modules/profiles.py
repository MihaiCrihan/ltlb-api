from src.modules.degrees.models import Degree
from src.modules.positions.models import Position
from src.modules.teacher.models import Teacher
from src.modules.users.models import User
from src.modules.profile.service import ProfileService

from src.app import db, app
from faker import Faker
from random import randint, choice

import string

letters = string.ascii_lowercase


def make_random_details(count=50):
    faker = Faker('ro_RO')

    return [
        {
            "title": faker.name(),
            "dates": [
                "2012-12-12"
            ],
            "credits": randint(1, 50)
        } for item in range(count)
    ]


def make_random_courses(count=50):
    faker = Faker('ro_RO')

    return [
        {
            "dates": [
                "2012-12-12"
            ],
            "credits": randint(1, 50),
            "name": faker.name(),
            "description": faker.sentence()
        } for item in range(count)
    ]


def make_random_positions(count=50):
    positions = Position.query.all()
    degrees = Degree.query.all()

    positions_ids = [item.id for item in positions]
    degrees_ids = [item.id for item in degrees]
    return [
        {
            "position_id": choice(positions_ids),
            "degree_id": choice(degrees_ids),
            "work_experience": randint(1, 40)
        } for item in range(count)
    ]


def make_teacher():
    faker = Faker('ro_RO')
    email = ''.join(choice(letters) for i in range(50))
    user = User(
        email=f'{email}@gmail.com',
        role_id=1,
        name=faker.name()
    )

    db.session.add(user)
    db.session.flush()
    teacher = Teacher(
        user_id=user.id,
        address=faker.address(),
        phone=faker.phone_number(),
        first_name=faker.first_name(),
        last_name=faker.last_name()
    )

    db.session.add(teacher)
    db.session.flush()

    return {
        "address": teacher.address,
        "id": teacher.id,
        "user_id": teacher.user_id,
        "phone": teacher.phone,
        "first_name": teacher.first_name,
        "last_name": teacher.last_name
    }


def make_profile():
    return {
        "teacher": make_teacher(),
        "courses": make_random_courses(),
        "positions": make_random_positions(),
        "details": make_random_details()
    }


class ProfileSeeder:
    seeder = []

    def __init__(self, count=5000):
        self.seeder = []
        self.name = __name__
        self.count = count
        self.profile_service = ProfileService()

    def __call__(self):
        with app.app_context():
            print("ProfilesSeeder is running...")

            for item in range(self.count):
                profile = make_profile()
                self.profile_service.update(profile['teacher']['user_id'], profile)
            db.session.commit()


profiles_seeder = ProfileSeeder(1000)
