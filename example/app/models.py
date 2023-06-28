from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship


class Asset(Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(512), nullable=False)
    owner_id = Column(Integer, ForeignKey('unit.id'))
    owner = relationship("Unit", backref="owner")
    date_time = Column(DateTime())
    date = Column(Date())

    def __repr__(self):
        return self.name


class Unit(Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(512), nullable=False)

    def __repr__(self):
        return self.name
