from flask import abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from setup import *
from models.user import User
from models.task import Task, TaskSchema
from blueprints.cli_bp import db_commands
from blueprints.users_bp import users_bp

def admin_required():
    user_email = get_jwt_identity()
    stmt = db.select(User).filter_by(email=user_email)
    user = db.session.scalar(stmt)
    if not (user and user.is_admin):
        abort(401)

@app.errorhandler(401)
def unauthorized(err):
    return {'error': 'You are not authorized to access this resource'}

app.register_blueprint(db_commands)

app.register_blueprint(users_bp)

@app.route('/task')
@jwt_required()
def all_cards():
    admin_required()
    # select * from task;
    stmt = db.select(Task)
    tasks = db.session.scalars(stmt).all()
    return TaskSchema(many=True).dump(tasks)