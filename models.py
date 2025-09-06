from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func

db = SQLAlchemy()

class thoughts_archive_test(db.Model):
    __tablename__ = "thoughts_archive_test"
    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String(255), nullable=True)
    title = Column(String(255), nullable=True)
    quote = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    actor = Column(String(255), nullable=True)
    image = Column(String(255))
    
    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "title": self.title,
            "actor": self.actor,
            "quote": self.quote,
            "image_url": self.image
        }