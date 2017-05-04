from conduit.database import (Model, SurrogatePK, db, Column,
                              reference_col, relationship)
import datetime as dt


class Article(SurrogatePK, Model):
    slug = Column(db.Text)
    title = Column(db.String(100), nullable=False)
    description = Column(db.Text)
    body = Column(db.Text)
    createdAt = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updatedAt = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    author = relationship('User', backref='articles')
    favoriters = relationship('User', backref='favorites')

    def __init__(self, author, title, body, **kwargs):
        db.Model.__init__(self, title=title, body=body, author=author, **kwargs)
