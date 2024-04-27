import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash


class Post(SqlAlchemyBase, SerializerMixin):
	__tablename__ = 'posts'

	id = sqlalchemy.Column(sqlalchemy.Integer, 
						   primary_key=True, autoincrement=True)
	content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
	created_date = sqlalchemy.Column(sqlalchemy.DateTime, 
									 default=datetime.datetime.now)
	creator_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

	creator = orm.relationship('User')
	comments = orm.relationship("Comment", back_populates='post')