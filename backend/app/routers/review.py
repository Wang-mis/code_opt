"""Review router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ..database import get_session
from ..models import Problem
from ..schemas import ProblemResponse

router = APIRouter(prefix="/review", tags=["review"])


@router.get("/random", response_model=ProblemResponse)
async def get_random_problem(
    session: AsyncSession = Depends(get_session),
):
    """Get a random problem for review."""
    # Count problems
    result = await session.execute(select(func.count(Problem.id)))
    count = result.scalar()

    if count == 0:
        raise HTTPException(status_code=404, detail="No problems available")

    # Get random problem
    import random
    offset = random.randint(0, count - 1)

    result = await session.execute(select(Problem).offset(offset).limit(1))
    problem = result.scalar_one_or_none()

    if not problem:
        raise HTTPException(status_code=404, detail="No problems available")

    return problem