from setup import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    tasks = db.relationship('Task', back_populates='user', cascade='all, delete')
    # cascade='all, delete' - when a user is deleted, all of their tasks are deleted

class UserSchema(ma.Schema):
    tasks = fields.Nested('TaskSchema', exclude=['user'], many=True)
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'is_admin', 'tasks')