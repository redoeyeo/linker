import os

from dotenv import load_dotenv
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.orm import DeclarativeBase, relationship

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    pass


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=True)
    content = Column(String, nullable=True)
    url = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship("Author", back_populates="articles")


class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=True)
    content = Column(String, nullable=True)
    url = Column(String, nullable=True)
    publication_date = Column(DateTime, nullable=True)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship("Author", back_populates="videos")


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=True)
    content = Column(String, nullable=True)
    url = Column(String, nullable=True)
    publication_year = Column(Integer, nullable=True)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship("Author", back_populates="books")


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    articles = relationship("Article", back_populates="author")
    videos = relationship("Video", back_populates="author")
    books = relationship("Book", back_populates="author")


Base.metadata.create_all(bind=engine)
