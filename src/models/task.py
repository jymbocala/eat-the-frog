from datetime import date
from setup import db, ma

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date_created = db.Column(db.Date, nullable=False, default=date.today())

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'date_created')