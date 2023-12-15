from models.follows import Follows
from setup import db, ma
from marshmallow import fields
from marshmallow.validate import Length, Regexp, And, Email


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
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
    # Tell Marshmallow to nest a TaskSchema instance when serializing the tasks attribute
    tasks = fields.Nested('TaskSchema', exclude=['user'], many=True)

    # Tell Marshmallow to nest a FollowsSchema instance when serializing the follows and followed_by attributes
    follows = fields.Nested('FollowsSchema', only=['following_id', 'followed_at'], many=True)
    followed_by = fields.Nested('FollowsSchema', only=['follower_id', 'followed_at'], many=True)

    # VALIDATION
    # name must be at least 1 character long and can only contain letters, spaces, and these characters: ,.'-
    name = fields.String(required=True, validate=And(Length(min=1), Regexp("^[a-zA-Z ,.'-]+$", error='Invalid name')))
    # email must be a valid email address
    email = fields.String(required=True, validate=Email(error='Invalid email address'))
    # password must be at least 6 characters long and must contain at least 1 letter, 1 number, and 1 special character
    password = fields.String(required=True, validate=Regexp("^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+]).{6,}$", error='Password must be at least 6 characters, 1 number, and 1 special character'))

    class Meta:
        fields = ('id', 'name', 'email', 'password', 'is_admin', 'total_tasks_completed', 'longest_streak', 'current_streak', 'tasks', 'follows', 'followed_by')