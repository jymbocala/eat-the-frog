from models.follows import Follows
from setup import db, ma
from marshmallow import fields
from sqlalchemy import event


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    total_tasks_completed = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)
    

    # SQLAlchemy relationship - nests an instance of a Task model in this one
    tasks = db.relationship('Task', back_populates='user', cascade='all, delete')
    # cascade='all, delete' - when a user is deleted, all of their tasks are deleted

    # SQLAlchemy relationship - nests an instance of a Follows model in this one
    follows = db.relationship('Follows', foreign_keys='Follows.follower_id', back_populates='follower', primaryjoin='User.id == Follows.follower_id')
    followed_by = db.relationship('Follows', foreign_keys='Follows.following_id', back_populates='following', primaryjoin='User.id == Follows.following_id')



class UserSchema(ma.Schema):
    tasks = fields.Nested('TaskSchema', exclude=['user'], many=True)
    
    follows = fields.Nested('FollowsSchema', only=['following_id', 'followed_at'], many=True)
    followed_by = fields.Nested('FollowsSchema', only=['follower_id', 'followed_at'], many=True)

    class Meta:
        fields = ('id', 'name', 'email', 'password', 'is_admin', 'total_tasks_completed', 'longest_streak', 'current_streak', 'tasks', 'follows', 'followed_by')