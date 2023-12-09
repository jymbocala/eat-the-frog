from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt


app = Flask(__name__)

# set the database URI via SQLAlchemy,
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://eat_the_frog_dev:spameggs123@127.0.0.1:5432/eat_the_frog_db'

# create the database object
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date_created = db.Column(db.Date)

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'date_created')

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'is_admin')

# CLI COMMANDS
@app.cli.command('db_create')
def db_create():
    db.drop_all()
    db.create_all()
    print('Created tables')


@app.cli.command('db_seed')
def db_seed():
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

    tasks = [
        Task(
        title='Complete Eat the Frog App Documentation',
        description='Complete the documentation for the Eat the Frog App and submit it to the Eat the Frog App Github repo.',
        date_created=date.today()
        ),
        Task(
        title='Finish Eat the Frog App',
        description='Finish the Eat the Frog App and submit it to the Eat the Frog App Github repo.',
        date_created=date.today()
        ),
    ]

    db.session.add_all(users)
    db.session.add_all(tasks)
    db.session.commit()

    print('Database seeded')


@app.route('/task')
def all_cards():
    # select * from task;
    stmt = db.select(Task)
    tasks = db.session.scalars(stmt).all()
    return TaskSchema(many=True).dump(tasks)


@app.route('/users/register', methods=['POST'])
def register():
    # Parse incoming POST body through the schema
    user_info = UserSchema(exclude=['id']).load(request.json)
    # Create a new user with the parsed data
    user = User(
        email=user_info['email'],
        password=bcrypt.generate_password_hash(user_info['password']).decode('utf8'),
        name=user_info.get('name', '')
    )

    # Add and commit the new user to the database
    db.session.add(user)
    db.session.commit()

    # Return the new user
    return UserSchema(exclude=['password']).dump(user), 201

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
