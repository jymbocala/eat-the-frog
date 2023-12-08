from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from datetime import date, datetime

app = Flask(__name__)

# set the database URI via SQLAlchemy, 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://eat_the_frog_dev:spameggs123@127.0.0.1:5432/eat_the_frog_db'

#create the database object
db = SQLAlchemy(app)



class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text())
    date_created = db.Column(db.Date, default=datetime.now().strftime('%Y-%m-%d'))


# CLI COMMANDS
@app.cli.command('db_create')
def db_create():
    db.drop_all()
    db.create_all()
    print('Created tables')


@app.cli.command('db_seed')
def db_seed():
    task = Task(
        title = 'Complete Eat the Frog App Documentation',
        description = 'Complete the documentation for the Eat the Frog App and submit it to the Eat the Frog App Github repo.',
        date_created = date.today()
    )

    db.session.add(task)
    db.session.commit()

    print('Database seeded')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"