from datetime import datetime
from setup import db, ma
from marshmallow import fields

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subtasks = db.Column(db.ARRAY(db.Text))
    is_completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.Date, default=datetime.now().strftime('%Y-%m-%d'))

    # Foreign key - establishes a relationship at the database level
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # SQLAlchemy relationship - nests an instance of a User model in this one
    user = db.relationship('User', back_populates='tasks')
    # back_populates - tells SQLAlchemy to look for a tasks attribute in the User model and use that to populate the user attribute in this model

class TaskSchema(ma.Schema):
    # Tell Marshmallow to nest a UserSchema instance when serializing
    user = fields.Nested('UserSchema', exclude=['password'])
    class Meta:
        fields = ('id', 'title', 'description', 'subtasks', 'is_completed', 'date_created', 'user')