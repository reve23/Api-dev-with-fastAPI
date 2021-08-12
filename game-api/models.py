from sqlalchemy import Column, Integer, String

from database import Base


class Games(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,index=True)
    description = Column(String)
    year = Column(Integer)
    image = Column(String)
