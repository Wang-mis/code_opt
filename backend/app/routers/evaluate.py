"""Evaluate router for code evaluation endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..models import Problem
from ..schemas import (
    EvaluateRequest,
    EvaluateResponse,
    BetterSolutionRequest,
    BetterSolutionResponse,
    OptimalSolutionRequest,
    OptimalSolutionResponse,
)
from ..services import evaluate_code, get_better_solution_hint, get_optimal_solution

router = APIRouter(prefix="/evaluate", tags=["evaluate"])


@router.post("", response_model=EvaluateResponse)
async def evaluate(
    data: EvaluateRequest,
    session: AsyncSession = Depends(get_session),
):
    """Submit code for evaluation."""
    # Get problem
    problem = await session.get(Problem, data.problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    # Evaluate code
    result = await evaluate_code(
        session=session,
        problem=problem,
        code=data.code,
        model_config=data.llm_config,
        session_id=data.session_id,
    )
    return result


@router.post("/better-solution", response_model=BetterSolutionResponse)
async def better_solution(
    data: BetterSolutionRequest,
    session: AsyncSession = Depends(get_session),
):
    """Get hint for a better solution."""
    # Get problem
    problem = await session.get(Problem, data.problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    result = await get_better_solution_hint(
        problem=problem,
        code=data.code,
        model_config=data.llm_config,
    )
    return result


@router.post("/answer", response_model=OptimalSolutionResponse)
async def get_answer(
    data: OptimalSolutionRequest,
    session: AsyncSession = Depends(get_session),
):
    """Get the optimal solution for a problem."""
    # Get problem
    problem = await session.get(Problem, data.problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    result = await get_optimal_solution(
        problem=problem,
        model_config=data.llm_config,
    )
    return result