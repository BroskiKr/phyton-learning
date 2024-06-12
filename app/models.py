from app.postgresDb import Base
from sqlalchemy import Column, Integer,String,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Post(Base):
  __tablename__ = "posts"
  
  id = Column(Integer,primary_key=True,nullable=False)
  title = Column(String,nullable=False)
  body = Column(String,nullable=False)
  created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
  owner_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
  owner = relationship("User")

# class User(Base):
#   __tablename__ = "users"

#   id = Column(Integer,primary_key=True,nullable=False)
#   first_name =  Column(String,nullable=False)
#   last_name =  Column(String,nullable=False)
#   email = Column(String,nullable=False)
#   password = Column(String,nullable=False,server_default=text('$2b$12$c/hk9viBU9LLX1I2FRcYGuijgxv6Js0gf3vV0rLfsiNkwJ/CmGeR.'))
#   created_at = Column(TIMESTAMP(timezone=True),server_default=text('now()'),nullable=False)