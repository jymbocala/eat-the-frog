from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from os import environ



app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = environ.get('JWT_KEY') 

# set the database URI via SQLAlchemy,
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://eat_the_frog_dev:spameggs123@127.0.0.1:5432/eat_the_frog_db'

# create the database object
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

def admin_required():
    user_email = get_jwt_identity()
    stmt = db.select(User).where(User.email == user_email)
    user = db.session.scalar(stmt)
    if not (user and user.is_admin):
        abort(401)

@app.errorhandler(401)
def unauthorized(err):
    return {'error': 'You are not authorized to access this resource'}


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date_created = db.Column(db.Date, nullable=False, default=date.today())

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
@jwt_required()
def all_cards():
    admin_required()
    # select * from task;
    stmt = db.select(Task)
    tasks = db.session.scalars(stmt).all()
    return TaskSchema(many=True).dump(tasks)


@app.route('/users/register', methods=['POST'])
def register():
    try:
        # Parse incoming POST body through the schema
        user_info = UserSchema(exclude=['id', 'is_admin']).load(request.json)
        # Create a new user with the parsed data
        user = User(
            email=user_info['email'],
            password=bcrypt.generate_password_hash(user_info['password']).decode('utf8'),
            name=user_info.get('name', '')
        )

        # Add and commit the new user to the database
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=user.email, expires_delta=timedelta(hours=2))

        return {'token': token, 'user': UserSchema(exclude=["password"]).dump(user)}, 201
    except IntegrityError:
        return {'error': 'Email already exists'}, 409

@app.route('/users/login', methods=['POST'])
def login():
    # 1. Parse incoming POST body through the schema
    user_info = UserSchema(exclude=['id', 'name', 'is_admin']).load(request.json)
    # 2. Select user with email that matches the one in the POST body
    stmt = db.select(User).where(User.email == user_info['email'])
    user = db.session.scalar(stmt)
    # 3. Check password hash
    if user and bcrypt.check_password_hash(user.password, user_info['password']):
        # 4. Create a JWT token
        token = create_access_token(identity=user.email, expires_delta=timedelta(hours=2))
        # 5. Return the token
        return {'token': token, 'user': UserSchema(exclude=['password']).dump(user)}
    else:
        return {'error': 'Invalid email or password'}, 401

