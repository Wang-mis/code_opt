"""Submissions router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..database import get_session
from ..models import Submission, LearningSession, Problem
from ..schemas import SubmissionResponse, LearningSessionResponse

router = APIRouter(prefix="/submissions", tags=["submissions"])


@router.get("", response_model=list[SubmissionResponse])
async def get_submissions(
    session: AsyncSession = Depends(get_session),
):
    """Get all submissions."""
    result = await session.execute(
        select(Submission)
        .options(selectinload(Submission.problem))
        .order_by(Submission.created_at.desc())
    )
    submissions = result.scalars().all()
    return submissions


@router.get("/{submission_id}", response_model=SubmissionResponse)
async def get_submission(
    submission_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Get a specific submission."""
    submission = await session.get(Submission, submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission


@router.get("/sessions/{session_id}", response_model=LearningSessionResponse)
async def get_learning_session(
    session_id: str,
    db_session: AsyncSession = Depends(get_session),
):
    """Get a learning session with all submissions."""
    result = await db_session.execute(
        select(LearningSession)
        .where(LearningSession.id == session_id)
        .options(selectinload(LearningSession.submissions))
    )
    learning_session = result.scalar_one_or_none()
    if not learning_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return learning_session