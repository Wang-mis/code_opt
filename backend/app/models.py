"""SQLAlchemy models for the database."""

from datetime import datetime
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
import uuid

from .database import Base


class SubmissionStatus(str, enum.Enum):
    """Status of a code submission."""
    PENDING = "pending"
    PERFECT = "perfect"
    HAS_ISSUES = "has_issues"


class SessionStatus(str, enum.Enum):
    """Status of a learning session."""
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    VIEWED_ANSWER = "viewed_answer"


class Problem(Base):
    """Problem model representing an algorithm problem."""
    __tablename__ = "problems"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationships
    submissions: Mapped[list["Submission"]] = relationship(
        "Submission",
        back_populates="problem",
        cascade="all, delete-orphan"
    )
    sessions: Mapped[list["LearningSession"]] = relationship(
        "LearningSession",
        back_populates="problem",
        cascade="all, delete-orphan"
    )


class Submission(Base):
    """Submission model representing a code submission."""
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    problem_id: Mapped[int] = mapped_column(Integer, ForeignKey("problems.id"), nullable=False)
    code: Mapped[str] = mapped_column(Text, nullable=False)
    evaluation: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[SubmissionStatus] = mapped_column(
        Enum(SubmissionStatus),
        default=SubmissionStatus.PENDING
    )
    iteration: Mapped[int] = mapped_column(Integer, default=1)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("learning_sessions.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    problem: Mapped["Problem"] = relationship("Problem", back_populates="submissions")
    session: Mapped["LearningSession"] = relationship("LearningSession", back_populates="submissions")


class LearningSession(Base):
    """Learning session model representing a learning session for a problem."""
    __tablename__ = "learning_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    problem_id: Mapped[int] = mapped_column(Integer, ForeignKey("problems.id"), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    final_status: Mapped[SessionStatus] = mapped_column(
        Enum(SessionStatus),
        nullable=True
    )

    # Relationships
    problem: Mapped["Problem"] = relationship("Problem", back_populates="sessions")
    submissions: Mapped[list["Submission"]] = relationship(
        "Submission",
        back_populates="session",
        cascade="all, delete-orphan"
    )