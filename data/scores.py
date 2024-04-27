import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Score(SqlAlchemyBase, SerializerMixin):
	__tablename__ = 'scores'

	id = sqlalchemy.Column(sqlalchemy.Integer, 
						   primary_key=True, autoincrement=True)
	value = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
	post_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
	user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

	user = orm.relationship('User')