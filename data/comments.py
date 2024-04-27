import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Comment(SqlAlchemyBase, SerializerMixin):
	__tablename__ = 'comments'

	id = sqlalchemy.Column(sqlalchemy.Integer, 
						   primary_key=True, autoincrement=True)
	content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
	post_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("posts.id"))
	user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

	post = orm.relationship('Post')