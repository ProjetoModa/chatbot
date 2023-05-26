from . import db
from sqlalchemy.sql import func


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(255), nullable=False, unique=True)
    state = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<Session {self.uuid}>'
