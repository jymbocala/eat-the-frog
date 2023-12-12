from datetime import datetime
from setup import db, ma
from marshmallow import fields

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date_created = db.Column(db.Date, default=datetime.now().strftime('%Y-%m-%d'))

    # Foreign key - establishes a relationship at the database level
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # SQLAlchemy relationship - nests an instance of a User model in this one
    user = db.relationship('User', back_populates='tasks')

class TaskSchema(ma.Schema):
    # Tell Marshmallow to nest a UserSchema instance when serializing
    user = fields.Nested('UserSchema', exclude=['password'])
    class Meta:
        fields = ('id', 'title', 'description', 'date_created', 'user')