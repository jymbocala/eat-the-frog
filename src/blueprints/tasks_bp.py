from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from setup import db
from models.task import TaskSchema, Task
from auth import admin_required

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

# get all tasks
@tasks_bp.route('/')
@jwt_required()
def all_tasks():
    admin_required()
    # select * from task;
    stmt = db.select(Task)
    tasks = db.session.scalars(stmt).all()
    return TaskSchema(many=True).dump(tasks)

# get one task
@tasks_bp.route('/<int:id>')
@jwt_required()
def one_task(id):
    admin_required()
    stmt = db.select(Task).filter_by(id=id) # .where(task.id == id)
    task = db.session.scalar(stmt)
    if task:
        return TaskSchema().dump(task)
    else:
        return {'error': 'Task not found'}, 404

# Create a new task
@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    task_info = TaskSchema(exclude=['id', 'date_created']).load(request.json)
    print(task_info)
    return "task created"