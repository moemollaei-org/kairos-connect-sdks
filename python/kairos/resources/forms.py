from __future__ import annotations
"""Forms resource for Kairos SDK."""

from typing import Any, Dict, Optional

from .._http import AsyncHttpClient, SyncHttpClient
from .._normalize import normalize_paginated, normalize_single, normalize_list
from ..types import Form, FormSubmission, PaginatedResponse


# ─── Async ───────────────────────────────────────────────────────────────────


class FormsResource:
    """Async forms resource."""

    def __init__(self, http_client: AsyncHttpClient):
        self._http = http_client

    # Core CRUD ----------------------------------------------------------------

    async def list(
        self,
        page: int = 1,
        limit: int = 20,
        is_active: Optional[bool] = None,
    ) -> PaginatedResponse[Form]:
        """List forms (requires read:forms scope)."""
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if is_active is not None:
            params["is_active"] = is_active

        response = await self._http.get("/forms/instances", params=params)
        return PaginatedResponse[Form](**normalize_paginated(response, 'instances', Form, limit=limit, offset=(page - 1) * limit))

    async def get(self, form_id: str) -> Form:
        """Get a single form by ID (requires read:forms scope)."""
        response = await self._http.get(f"/forms/instances/{form_id}")
        return normalize_single(response, 'instance', Form)

    async def create(
        self,
        name: str,
        description: Optional[str] = None,
        fields: Optional[list] = None,
        settings: Optional[Dict[str, Any]] = None,
        is_active: bool = True,
    ) -> Form:
        """Create a new form (requires write:forms scope)."""
        data: Dict[str, Any] = {"name": name, "is_active": is_active}
        if description:
            data["description"] = description
        if fields is not None:
            data["fields"] = fields
        if settings is not None:
            data["settings"] = settings

        response = await self._http.post("/forms/instances", json_data=data)
        return normalize_single(response, 'instance', Form)

    async def update(
        self,
        form_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        fields: Optional[list] = None,
        settings: Optional[Dict[str, Any]] = None,
        is_active: Optional[bool] = None,
    ) -> Form:
        """Update a form (requires write:forms scope)."""
        data: Dict[str, Any] = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if fields is not None:
            data["fields"] = fields
        if settings is not None:
            data["settings"] = settings
        if is_active is not None:
            data["is_active"] = is_active

        response = await self._http.put(f"/forms/instances/{form_id}", json_data=data)
        return normalize_single(response, 'instance', Form)

    async def delete(self, form_id: str) -> None:
        """Delete a form (requires write:forms scope)."""
        await self._http.delete(f"/forms/instances/{form_id}")

    # Submissions --------------------------------------------------------------

    async def list_submissions(
        self, form_id: str, page: int = 1, limit: int = 20
    ) -> PaginatedResponse[FormSubmission]:
        """List submissions for a form (requires read:forms scope)."""
        params = {"page": page, "limit": limit}
        response = await self._http.get(f"/forms/instances/{form_id}/records", params=params)
        return PaginatedResponse[FormSubmission](**normalize_paginated(response, 'records', FormSubmission, limit=limit, offset=(page - 1) * limit))

    async def submit(
        self,
        form_id: str,
        data: Dict[str, Any],
    ) -> FormSubmission:
        """Submit a response to a form (requires write:forms scope)."""
        response = await self._http.post(
            f"/forms/instances/{form_id}/records",
            json_data={"data": data},
        )
        return normalize_single(response, 'record', FormSubmission)


# ─── Sync ────────────────────────────────────────────────────────────────────


class SyncFormsResource:
    """Synchronous forms resource."""

    def __init__(self, http_client: SyncHttpClient):
        self._http = http_client

    # Core CRUD ----------------------------------------------------------------

    def list(
        self,
        page: int = 1,
        limit: int = 20,
        is_active: Optional[bool] = None,
    ) -> PaginatedResponse[Form]:
        """List forms."""
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if is_active is not None:
            params["is_active"] = is_active

        response = self._http.get("/forms/instances", params=params)
        return PaginatedResponse[Form](**normalize_paginated(response, 'instances', Form, limit=limit, offset=(page - 1) * limit))

    def get(self, form_id: str) -> Form:
        """Get a single form by ID."""
        response = self._http.get(f"/forms/instances/{form_id}")
        return normalize_single(response, 'instance', Form)

    def create(
        self,
        name: str,
        description: Optional[str] = None,
        fields: Optional[list] = None,
        settings: Optional[Dict[str, Any]] = None,
        is_active: bool = True,
    ) -> Form:
        """Create a new form."""
        data: Dict[str, Any] = {"name": name, "is_active": is_active}
        if description:
            data["description"] = description
        if fields is not None:
            data["fields"] = fields
        if settings is not None:
            data["settings"] = settings

        response = self._http.post("/forms/instances", json_data=data)
        return normalize_single(response, 'instance', Form)

    def update(
        self,
        form_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        fields: Optional[list] = None,
        settings: Optional[Dict[str, Any]] = None,
        is_active: Optional[bool] = None,
    ) -> Form:
        """Update a form."""
        data: Dict[str, Any] = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if fields is not None:
            data["fields"] = fields
        if settings is not None:
            data["settings"] = settings
        if is_active is not None:
            data["is_active"] = is_active

        response = self._http.put(f"/forms/instances/{form_id}", json_data=data)
        return normalize_single(response, 'instance', Form)

    def delete(self, form_id: str) -> None:
        """Delete a form."""
        self._http.delete(f"/forms/instances/{form_id}")

    # Submissions --------------------------------------------------------------

    def list_submissions(
        self, form_id: str, page: int = 1, limit: int = 20
    ) -> PaginatedResponse[FormSubmission]:
        """List submissions for a form."""
        params = {"page": page, "limit": limit}
        response = self._http.get(f"/forms/instances/{form_id}/records", params=params)
        return PaginatedResponse[FormSubmission](**normalize_paginated(response, 'records', FormSubmission, limit=limit, offset=(page - 1) * limit))

    def submit(
        self,
        form_id: str,
        data: Dict[str, Any],
    ) -> FormSubmission:
        """Submit a response to a form."""
        response = self._http.post(
            f"/forms/instances/{form_id}/records",
            json_data={"data": data},
        )
        return normalize_single(response, 'record', FormSubmission)
