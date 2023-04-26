import datetime
import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class CDEL(SqlAlchemyBase):
    __tablename__ = 'cdel'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    typef = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    price_type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    pr_fio = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    po_fio = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    pr_data = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    po_data = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    pr_cer = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    pr_no = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    po_cer = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    po_no = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')