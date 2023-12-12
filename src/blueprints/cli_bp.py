from flask import Blueprint
from setup import db, bcrypt
from models.task import Task
from models.user import User
from datetime import date

db_commands = Blueprint('db', __name__)

# CLI COMMANDS
@db_commands.cli.command('create')
def db_create():
    db.drop_all()
    db.create_all()
    print('Created tables')


@db_commands.cli.command('seed')
def db_seed():
    
    # Users
    users = [
        User(
            name='Giddig Nor',
            email='admin@spam.com',
            password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin=True
        ),
        User(
            name='Jav Ascripp',
            email='jav@spam.com',
            password=bcrypt.generate_password_hash('javascript123').decode('utf-8')
        )
    ]

    db.session.add_all(users)
    db.session.commit()

    # Tasks
    tasks = [
        Task(
        title='Complete Eat the Frog App Documentation',
        description='Complete the documentation for the Eat the Frog App and submit it to the Eat the Frog App Github repo.',
        date_created=date.today(),
        user_id = users[0].id
        ),
        Task(
        title='Finish Eat the Frog App',
        description='Finish the Eat the Frog App and submit it to the Eat the Frog App Github repo.',
        date_created=date.today(),
        user_id = users[1].id
        ),
    ]

    db.session.add_all(tasks)
    db.session.commit()

    print('Database seeded')
