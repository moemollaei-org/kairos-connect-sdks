from __future__ import annotations
"""Kairos SDK — Official Python client for the Kairos API."""

__version__ = "0.3.0"

from .client import Kairos, KairosSync
from .errors import (
    KairosError,
    AuthError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ValidationError,
    InternalError,
)

__all__ = [
    "Kairos",
    "KairosSync",
    "KairosError",
    "AuthError",
    "ForbiddenError",
    "NotFoundError",
    "RateLimitError",
    "ValidationError",
    "InternalError",
]
