from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func
from quart_auth import AuthUser

Base = declarative_base()


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True)
    filename = Column(String(100), nullable=False)
    namePicture = Column(String(100), nullable=False)
    filepath = Column(String(200), nullable=False)
    timestamp = Column(DateTime, server_default=func.now())


class User(Base, AuthUser):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(150), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(60), nullable=False)

    # @property
    def loader_user(self):
        return self.id

    def __repr__(self):
        return f"User( %r)" % self.email
