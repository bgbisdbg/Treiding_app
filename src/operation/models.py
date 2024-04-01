from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData
from sqlalchemy.ext.declarative import declarative_base

from database import Base


class Operation(Base):
    __tablename__= 'operation'

    id = Column(Integer, primary_key=True)
    quantity = Column(String)
    figi = Column(String)
    instrument_type = Column(String, nullable=True)
    date = Column(TIMESTAMP)
    type = Column(String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}