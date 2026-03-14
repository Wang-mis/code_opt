"""Problems router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_session
from ..models import Problem
from ..schemas import ProblemCreate, ProblemUpdate, ProblemResponse

router = APIRouter(prefix="/problems", tags=["problems"])


@router.get("", response_model=list[ProblemResponse])
async def get_problems(
    session: AsyncSession = Depends(get_session),
):
    """Get all problems."""
    result = await session.execute(select(Problem).order_by(Problem.created_at.desc()))
    problems = result.scalars().all()
    return problems


@router.get("/{problem_id}", response_model=ProblemResponse)
async def get_problem(
    problem_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Get a specific problem."""
    problem = await session.get(Problem, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem


@router.post("", response_model=ProblemResponse)
async def create_problem(
    data: ProblemCreate,
    session: AsyncSession = Depends(get_session),
):
    """Create a new problem."""
    problem = Problem(
        title=data.title,
        description=data.description,
    )
    session.add(problem)
    await session.commit()
    await session.refresh(problem)
    return problem


@router.put("/{problem_id}", response_model=ProblemResponse)
async def update_problem(
    problem_id: int,
    data: ProblemUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Update a problem."""
    problem = await session.get(Problem, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    problem.title = data.title
    problem.description = data.description
    await session.commit()
    await session.refresh(problem)
    return problem


@router.delete("/{problem_id}")
async def delete_problem(
    problem_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Delete a problem."""
    problem = await session.get(Problem, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    await session.delete(problem)
    await session.commit()
    return {"message": "Problem deleted"}