from setup import app
from blueprints.cli_bp import db_commands
from blueprints.users_bp import users_bp
from blueprints.tasks_bp import tasks_bp
from blueprints.follows_bp import follows_bp

# Register blueprints
app.register_blueprint(db_commands)
app.register_blueprint(users_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(follows_bp)


print(app.url_map)