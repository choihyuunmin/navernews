from sqlite3 import Date
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Sequence
from sqlalchemy.sql.expression import text

from database import Base




class Articles(Base):
    __tablename__ = "tb_article"
    id = Column(Integer, Sequence('seq_article'), primary_key=True, nullable=False)
    title = Column(String(256))
    url = Column(String(512))
    reg_date = Column(DateTime(timezone=True), nullable=True, server_defalut=text("now()"))


class Comments(Base):
    __tablename__ = "tb_comment"
    id = Column(Integer, Sequence('seq_article'), primary_key=True, nullable=False)
    comments = Column(String(1024), nullable=False)
    reg_date = Column(DateTime(timezone=True))




