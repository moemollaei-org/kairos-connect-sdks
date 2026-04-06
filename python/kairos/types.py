from __future__ import annotations
"""Pydantic models for Kairos API responses."""

from typing import Any, Dict, Generic, List, Literal, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


# ─── Shared / pagination ──────────────────────────────────────────────────────


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


# ─── Task models ──────────────────────────────────────────────────────────────


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
    actual_hours: Optional[float] = None
    due_date: Optional[str] = None
    start_date: Optional[str] = None
    completed_at: Optional[str] = None
    order_index: int = 0
    is_recurring: bool = False
    recurrence_rule: Optional[str] = None
    created_by: str
    created_at: str
    updated_at: str


class TaskAssignee(BaseModel):
    """Task assignee — record from task_assignees table."""

    task_id: str
    user_id: str
    assigned_by: str
    assigned_at: str


class TaskLabel(BaseModel):
    """Task label — record from task_labels table."""

    task_id: str
    label_id: str
    added_by: str
    added_at: str


class TaskDependency(BaseModel):
    """Task dependency — record from task_dependencies table."""

    id: str
    task_id: str
    depends_on_task_id: str
    dependency_type: Literal["blocks", "blocked_by", "relates_to", "duplicates"]
    created_by: str
    created_at: str


# ─── Goal models ──────────────────────────────────────────────────────────────


class Goal(BaseModel):
    """Goal model."""

    id: str
    team_id: str
    title: str
    description: Optional[str] = None
    status: Literal["active", "completed", "archived"] = "active"
    progress: float = 0.0
    due_date: Optional[str] = None
    start_date: Optional[str] = None
    owner_id: Optional[str] = None
    created_by: str
    created_at: str
    updated_at: str


# ─── Comment model ────────────────────────────────────────────────────────────


class Comment(BaseModel):
    """Comment on any entity (task, goal, document, whiteboard, or form)."""

    id: str
    team_id: str
    entity_type: Optional[Literal["task", "goal", "document", "whiteboard", "form"]] = None
    entity_id: Optional[str] = None
    task_id: Optional[str] = None
    goal_id: Optional[str] = None
    parent_comment_id: Optional[str] = None
    content: str
    created_by: str
    created_at: str
    updated_at: str


# ─── Document models ──────────────────────────────────────────────────────────


class Document(BaseModel):
    """Document model (Notion-like rich text page or database)."""

    id: str
    team_id: str
    teamspace_id: Optional[str] = None
    parent_id: Optional[str] = None
    title: str
    content: Optional[Dict[str, Any]] = None
    type: Literal["document", "database", "page"] = "document"
    icon: Optional[str] = None
    cover_image: Optional[str] = None
    is_public: bool = False
    word_count: int = 0
    created_by: str
    last_edited_by: Optional[str] = None
    created_at: str
    updated_at: str


# ─── Whiteboard models ────────────────────────────────────────────────────────


class Whiteboard(BaseModel):
    """Whiteboard model."""

    id: str
    team_id: str
    title: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    is_public: bool = False
    created_by: str
    created_at: str
    updated_at: str


# ─── Form models (CRM form configs + submissions) ─────────────────────────────


class FormField(BaseModel):
    """Individual field definition within a form."""

    id: str
    type: Literal["text", "email", "phone", "number", "select", "multiselect", "checkbox", "date", "textarea"]
    label: str
    placeholder: Optional[str] = None
    required: bool = False
    options: Optional[List[str]] = None


class Form(BaseModel):
    """Form configuration model (crm_form_configs)."""

    id: str
    team_id: str
    name: str
    description: Optional[str] = None
    fields: List[FormField] = []
    settings: Dict[str, Any] = {}
    is_active: bool = True
    submission_count: int = 0
    created_by: str
    created_at: str
    updated_at: str


class FormSubmission(BaseModel):
    """A single form submission (crm_form_submissions)."""

    id: str
    form_id: str
    team_id: str
    data: Dict[str, Any]
    submitter_email: Optional[str] = None
    submitter_name: Optional[str] = None
    ip_address: Optional[str] = None
    submitted_at: str


# ─── Team models ──────────────────────────────────────────────────────────────


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


# ─── Auth / config ────────────────────────────────────────────────────────────


class MeResponse(BaseModel):
    """Current user/auth response."""

    team_id: str
    scopes: List[str]
    rate_limit_per_minute: int
    rate_limit_per_hour: int
