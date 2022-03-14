from src.modules.users.models import User
from datetime import datetime as dt
data = [
    {
        "name": "Tudor",
        "email": 'teisanutudort@gmail.com',
        "password": "12345678"
    }
]


class UsersSeeder:
    users_seeder = []

    def __call__(self):
        for item in data:
            user = User()
            user.name = item['name']
            user.email = item['email']
            user.is_active = True
            user.confirmed_at = dt.now().isoformat()
            user.password_hash = user.hash_password(item['password'])
            self.users_seeder.append(user)

        return self.users_seeder


users_seeder = UsersSeeder()