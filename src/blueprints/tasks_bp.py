from datetime import datetime
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from setup import db
from models.task import TaskSchema, Task
from auth import authorize

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

# Get all tasks (for the current user)
@tasks_bp.route('/')
@jwt_required()
def all_tasks():
    current_user_id = get_jwt_identity()  # Get the user ID from the JWT token
    
    # Select all tasks for the current user
    stmt = db.select(Task).where(Task.user_id == current_user_id)
    # Execute the query and return the results
    tasks = db.session.scalars(stmt).all()

    # Exclude the nested fields from the UserSchema
    return TaskSchema(many=True, exclude=['user.tasks', 'user.follows', 'user.followed_by', 'user.is_admin', 'user.email']).dump(tasks)

# Get one task
@tasks_bp.route('/<int:id>')
@jwt_required()
def one_task(id):
    stmt = db.select(Task).filter_by(id=id)
    task = db.session.scalar(stmt)
    if task:
        authorize(task.user_id)

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
    # Get the current user ID
    user_id = get_jwt_identity()

    # Check if a task already exists for the current day
    today = datetime.today().date()
    existing_task = Task.query.filter_by(user_id=user_id, date_created=today).first()

    if existing_task:
        return {'error': 'You can only create one task per day'}, 400

    # Parse incoming POST body through the schema
    task_info = TaskSchema().load(request.json)

    # Create a new task
    new_task = Task(
        title=task_info['title'],
        description=task_info['description'],
        subtasks=task_info.get('subtasks', []), # subtasks with default value as an empty list
        date_created=today,
        user_id=user_id
    )

    db.session.add(new_task)
    db.session.commit()

    return TaskSchema(exclude=['user.tasks', 'user.follows', 'user.followed_by', 'user.is_admin', 'user.email']).dump(new_task), 201

# Update a task
@tasks_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_task(id):

    # Parse incoming PUT body through the schema
    task_info = TaskSchema(exclude=['id', 'date_created']).load(request.json)
    stmt = db.select(Task).filter_by(id=id)
    task = db.session.scalar(stmt)
    if task:
        authorize(task.user_id)

        # Update the task with the new information from the request body
        task.title = task_info.get('title', task.title)
        task.description = task_info.get('description', task.description)
        task.subtasks = task_info.get('subtasks', task.subtasks)
        task.is_completed = task_info.get('is_completed', task.is_completed)

        db.session.commit()
        return TaskSchema(exclude=['user.tasks', 'user.follows', 'user.followed_by', 'user.is_admin', 'user.email']).dump(task)
    else:
        return {'error': 'Task not found'}, 404
    
# Delete a task
@tasks_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    stmt = db.select(Task).filter_by(id=id) # get the task with the specified id
    task = db.session.scalar(stmt)
    if task:
        authorize(task.user_id) # Check if the user is the owner of the task
        db.session.delete(task)
        db.session.commit()
        return {'message': 'Task deleted successfully.'}
    else:
        return {'error': 'Task not found'}, 404
    
