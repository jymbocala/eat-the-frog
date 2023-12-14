from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from setup import db
from models.follows import Follows
from models.user import User

follows_bp = Blueprint("follows", __name__, url_prefix="/users")


@follows_bp.route("/<int:user_id>/follow", methods=["POST"])
@jwt_required()
def follow_user(user_id):
    current_user_id = get_jwt_identity()

    if user_id == current_user_id:
        return {"error": "Cannot follow yourself"}, 400

    # Check if the user to be followed exists
    user_to_follow = User.query.get(user_id)
    if not user_to_follow:
        return {"error": "User not found"}, 404

    # Check if the follow relationship already exists
    existing_follow = Follows.query.filter_by(follower_id=current_user_id, following_id=user_id).first()
    if existing_follow:
        return {"error": "Already following this user"}, 400

    # Create a new follow relationship
    new_follow = Follows(follower_id=current_user_id, following_id=user_id)
    db.session.add(new_follow)
    db.session.commit()

    return {"message": "User followed successfully"}, 200


@follows_bp.route("/<int:user_id>/unfollow", methods=["POST"])
@jwt_required()
def unfollow_user(user_id):
    current_user_id = get_jwt_identity()

    if user_id == current_user_id:
        return {"error": "Cannot unfollow yourself"}, 400

    # Check if the user to be unfollowed exists
    user_to_unfollow = User.query.get(user_id)
    if not user_to_unfollow:
        return {"error": "User not found"}, 404

    # Check if the follow relationship exists
    existing_follow = Follows.query.filter_by(follower_id=current_user_id, following_id=user_id).first()
    if not existing_follow:
        return {"error": "Not following this user"}, 400

    # Remove the follow relationship
    db.session.delete(existing_follow)
    db.session.commit()

    return {"message": "User unfollowed successfully"}, 200