from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    title = Column(String)
    messages = relationship("Message", back_populates="chat")
    analyses = relationship("Analysis", back_populates="chat")

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    role = Column(String)  # 'user' or 'assistant'
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    chat = relationship("Chat", back_populates="messages")

class Analysis(Base):
    __tablename__ = 'analyses'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    analysis_type = Column(String)
    visualization_type = Column(String)
    data_summary = Column(JSON)
    insights = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    chart_path = Column(String)
    chat = relationship("Chat", back_populates="analyses")

def init_db(db_url: str = "sqlite:///./chatplot.db"):
    """Initialize the database"""
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine 