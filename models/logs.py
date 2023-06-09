from . import db
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import LONGTEXT

class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(LONGTEXT, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    
    def __repr__(self):
        return f'<Logs {self.name}>'
