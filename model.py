from app import app, db
import os
from datetime import datetime

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete =  db.Column(db.Integer, default=0)
    created =  db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'< Task {self.id}>'