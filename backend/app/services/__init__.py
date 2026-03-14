"""Services package."""
from .llm_service import (
    evaluate_code,
    get_better_solution_hint,
    get_optimal_solution,
)

__all__ = [
    "evaluate_code",
    "get_better_solution_hint",
    "get_optimal_solution",
]