from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime, BigInteger, JSON, Enum as SQLEnum
from sqlalchemy.types import Uuid
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone
import uuid
import enum

Base = declarative_base()

def generate_uuid():
    return uuid.uuid4()

def utc_now():
    return datetime.now(timezone.utc)

class GameType(str, enum.Enum):
    MULTIPLE_CHOICE = 'MULTIPLE_CHOICE'
    ANAGRAM = 'ANAGRAM'
    SPEED_MATCH = 'SPEED_MATCH'

class MasteryStatus(str, enum.Enum):
    LOCKED = 'LOCKED'
    UNLOCKED = 'UNLOCKED'
    MASTERED = 'MASTERED'

class User(Base):
    __tablename__ = "users"
    id = Column(Uuid, primary_key=True, default=generate_uuid)
    telegram_id = Column(BigInteger, unique=True, index=True)
    grade_level = Column(Integer, nullable=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    total_xp = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    last_active_date = Column(DateTime(timezone=True), nullable=True)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Uuid, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True, index=True)
    suggested_grade = Column(Integer, nullable=True)
    prerequisite_topic_ids = Column(JSON, nullable=True) # Array of UUIDs stored as JSON
    is_nmt_relevant = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

class Question(Base):
    __tablename__ = "questions"
    id = Column(Uuid, primary_key=True, default=generate_uuid)
    topic_id = Column(Uuid, ForeignKey("topics.id"))
    game_type = Column(SQLEnum(GameType), default=GameType.MULTIPLE_CHOICE)
    baseline_elo = Column(Integer, default=1000)
    content = Column(JSON) # e.g. {"text": "...", "options": {"A": "1", ...}}
    validation_rules = Column(JSON) # e.g. {"correct_option": "A"}
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    
    topic = relationship("Topic")

class UserTopicMastery(Base):
    __tablename__ = "user_topic_mastery"
    user_id = Column(Uuid, ForeignKey("users.id"), primary_key=True)
    topic_id = Column(Uuid, ForeignKey("topics.id"), primary_key=True)
    status = Column(SQLEnum(MasteryStatus), default=MasteryStatus.LOCKED)
    elo_rating = Column(Integer, default=1000)
    accuracy_rate = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

class GameSession(Base):
    __tablename__ = "game_sessions"
    id = Column(Uuid, primary_key=True, default=generate_uuid)
    user_id = Column(Uuid, ForeignKey("users.id"))
    question_id = Column(Uuid, ForeignKey("questions.id"))
    is_correct = Column(Boolean)
    time_taken_ms = Column(Integer, nullable=True)
    awarded_xp = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
