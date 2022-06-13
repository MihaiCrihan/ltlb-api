from src.modules.degrees.models import Degree
from src.app import db, app
from faker import Faker

data = [
    {
        "name": "Fara grad"
    },
    {
        "name": "Grad I"
    },
    {
        "name": "Grad II"
    },
    {
        "name": "Grad superior"
    }
]


class DegreesSeeder:
    seeder = []

    def __init__(self, count=5000):
        self.seeder = []
        self.name = __name__
        self.count = count

    def __call__(self):
        with app.app_context():
            print("DegreesSeeder is running...")
            for item in data:
                if not (Degree.query.filter_by(name=item['name']).first()):
                    self.seeder.append(Degree(name=item['name']))

            for item in range(self.count):
                faker = Faker('ro_RO')
                self.seeder.append(Degree(name=faker.name()))

            db.session.add_all(self.seeder)
            db.session.commit()


degree_seeder = DegreesSeeder(500)
