from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from setup import db
from models.task import TaskSchema, Task
from auth import admin_required

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

# Get all tasks
@tasks_bp.route('/')
@jwt_required()
def all_tasks():
    # admin_required()
    # select * from task;
    stmt = db.select(Task)
    tasks = db.session.scalars(stmt).all()
    return TaskSchema(many=True, exclude=['user.tasks', 'user.follows', 'user.followed_by', 'user.is_admin', 'user.email']).dump(tasks)

# Get one task
@tasks_bp.route('/<int:id>')
@jwt_required()
def one_task(id):
    # admin_required()
    stmt = db.select(Task).filter_by(id=id) # .where(task.id == id)
    task = db.session.scalar(stmt)
    if task:
        # Specify the fields you want to include in the nested UserSchema
        include_user_fields = ['id', 'name']

        # Use the only parameter to include specific fields in the nested UserSchema
        task_schema = TaskSchema()
        task_schema.fields['user'].only = include_user_fields

        return task_schema.dump(task)
    else:
        return {'error': 'Task not found'}, 404

# Create a new task
@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    task_info = TaskSchema(exclude=['id','is_completed', 'date_created']).load(request.json)
    task = Task(
        title=task_info['title'],
        description=task_info['description'],
        subtasks=task_info['subtasks']
    )

    db.session.add(task)
    db.session.commit()
    return TaskSchema().dump(task), 201

# Update a task
@tasks_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_task(id):
    task_info = TaskSchema(exclude=['id', 'date_created']).load(request.json)
    stmt = db.select(Task).filter_by(id=id) # .where(Task.id == id)
    task = db.session.scalar(stmt)
    if task:
        task.title = task_info.get('title', task.title)
        task.description = task_info.get('description', task.description)
        task.subtasks = task_info.get('subtasks', task.subtasks)
        task.is_complete = task_info.get('is_complete', task.is_complete)

        db.session.commit()
        return TaskSchema().dump(task)
    else:
        return {'error': 'Task not found'}, 404
    
# Delete a task
@tasks_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    # admin_required()
    stmt = db.select(Task).filter_by(id=id) # .where(Task.id == id)
    task = db.session.scalar(stmt)
    if task:
        db.session.delete(task)
        db.session.commit()
        return 'Task deleted', 200
    else:
        return {'error': 'Task not found'}, 404
    
