"""Pydantic schemas for API request/response validation."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from .models import SubmissionStatus, SessionStatus


# Model Configuration
class ModelConfig(BaseModel):
    """Configuration for the LLM model."""
    provider: str = Field(..., description="Model provider (e.g., openai, anthropic)")
    model: str = Field(..., description="Model name")
    api_key: str = Field(..., description="API key for the provider")
    base_url: Optional[str] = Field(None, description="Custom base URL")


# Problem schemas
class ProblemBase(BaseModel):
    """Base schema for Problem."""
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)


class ProblemCreate(ProblemBase):
    """Schema for creating a problem."""
    pass


class ProblemUpdate(ProblemBase):
    """Schema for updating a problem."""
    pass


class ProblemResponse(ProblemBase):
    """Schema for problem response."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# Submission schemas
class SubmissionCreate(BaseModel):
    """Schema for creating a submission."""
    problem_id: int
    code: str = Field(..., min_length=1)
    session_id: Optional[str] = None
    llm_config: ModelConfig


class SubmissionResponse(BaseModel):
    """Schema for submission response."""
    id: int
    problem_id: int
    code: str
    evaluation: Optional[str] = None
    status: SubmissionStatus
    iteration: int
    session_id: str
    created_at: datetime
    problem: Optional[ProblemResponse] = None

    model_config = {"from_attributes": True}


# Learning Session schemas
class LearningSessionResponse(BaseModel):
    """Schema for learning session response."""
    id: str
    problem_id: int
    problem: Optional[ProblemResponse] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    final_status: Optional[SessionStatus] = None
    submissions: list[SubmissionResponse] = []

    model_config = {"from_attributes": True}


# Evaluation schemas
class EvaluateRequest(BaseModel):
    """Request for code evaluation."""
    problem_id: int
    code: str
    session_id: Optional[str] = None
    llm_config: ModelConfig


class EvaluateResponse(BaseModel):
    """Response for code evaluation."""
    evaluation: str
    status: SubmissionStatus
    submission_id: int


class BetterSolutionRequest(BaseModel):
    """Request for better solution hint."""
    problem_id: int
    code: str
    llm_config: ModelConfig


class BetterSolutionResponse(BaseModel):
    """Response for better solution hint."""
    hint: str


class OptimalSolutionRequest(BaseModel):
    """Request for optimal solution."""
    problem_id: int
    llm_config: ModelConfig


class OptimalSolutionResponse(BaseModel):
    """Response for optimal solution."""
    code: str
    explanation: str