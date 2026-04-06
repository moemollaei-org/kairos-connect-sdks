"""Pydantic models for Kairos API responses."""

from typing import Any, Generic, List, Literal, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Pagination(BaseModel):
    """Pagination metadata for list responses."""

    page: int
    limit: int
    total: int
    has_more: bool


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper."""

    data: List[T]
    pagination: Pagination


class SingleResponse(BaseModel, Generic[T]):
    """Generic single-item response wrapper."""

    data: T


class Task(BaseModel):
    """Task model."""

    id: str
    team_id: str
    goal_id: Optional[str] = None
    parent_task_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    type: Literal["task", "sub_task", "bug", "story", "epic"] = "task"
    status: Literal["to_do", "in_progress", "in_review", "completed", "cancelled"] = "to_do"
    priority: Literal["low", "medium", "high", "urgent"] = "medium"
    assigned_to: Optional[str] = None
    estimated_hours: Optional[float] = None
    due_date: Optional[str] = None
    completed_at: Optional[str] = None
    created_by: str
    created_at: str
    updated_at: str


class Goal(BaseModel):
    """Goal model."""

    id: str
    team_id: str
    title: str
    description: Optional[str] = None
    status: Literal["active", "completed", "archived"] = "active"
    progress: float = 0.0
    due_date: Optional[str] = None
    created_by: str
    created_at: str
    updated_at: str


class Comment(BaseModel):
    """Comment model."""

    id: str
    task_id: str
    team_id: str
    content: str
    created_by: str
    created_at: str
    updated_at: str


class Team(BaseModel):
    """Team model."""

    id: str
    name: str
    slug: str
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: str


class TeamMember(BaseModel):
    """Team member model."""

    user_id: str
    email: str
    name: str
    avatar_url: Optional[str] = None
    role: str
    joined_at: str


class Document(BaseModel):
    """Document model."""

    id: str
    team_id: str
    title: str
    content: Optional[str] = None
    created_by: str
    created_at: str
    updated_at: str


class MeResponse(BaseModel):
    """Current user/auth response."""

    team_id: str
    scopes: List[str]
    rate_limit_per_minute: int
    rate_limit_per_hour: int
