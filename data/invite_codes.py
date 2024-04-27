import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
import random
import string


class InviteCode(SqlAlchemyBase, SerializerMixin):
	__tablename__ = 'invite_codes'

	id = sqlalchemy.Column(sqlalchemy.Integer, 
						   primary_key=True, autoincrement=True)
	code = sqlalchemy.Column(sqlalchemy.String, nullable=True)
	used = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
	created_date = sqlalchemy.Column(sqlalchemy.DateTime, 
									 default=datetime.datetime.now)