"""Review router."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ..database import get_session
from ..models import Problem
from ..schemas import ProblemResponse

router = APIRouter(prefix="/review", tags=["review"])


@router.get("/random", response_model=ProblemResponse)
async def get_random_problem(
    session: AsyncSession = Depends(get_session),
    exclude_id: int | None = Query(default=None, description="Problem ID to exclude"),
):
    """Get a random problem for review."""
    # Build query with optional exclusion
    base_query = select(Problem)
    if exclude_id is not None:
        base_query = base_query.where(Problem.id != exclude_id)

    # Count problems
    count_query = select(func.count(Problem.id))
    if exclude_id is not None:
        count_query = count_query.where(Problem.id != exclude_id)

    result = await session.execute(count_query)
    count = result.scalar()

    if count == 0:
        raise HTTPException(status_code=404, detail="No problems available")

    # Get random problem
    import random
    offset = random.randint(0, count - 1)

    result = await session.execute(base_query.offset(offset).limit(1))
    problem = result.scalar_one_or_none()

    if not problem:
        raise HTTPException(status_code=404, detail="No problems available")

    return problem