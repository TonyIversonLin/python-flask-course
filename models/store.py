import sqlite3

from db import db

class StoreModel(db.Model):

    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name) -> None:
        self.name = name

    def json(self): 
        return {'name': self.name, 'items': [item.json() for item in self.items.all()], 'id': self.id}

    
    @classmethod
    def find_by_name(cls, name):
        return StoreModel.query.filter_by(name=name).first()   # SELECT * FROM items WHERE name=@name

    def save_to_db(self):    # can handle both update annd post
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()