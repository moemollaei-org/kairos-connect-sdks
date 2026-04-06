from __future__ import annotations
"""Internal HTTP client for Kairos SDK."""

import asyncio
import json
from typing import Any, Dict, Optional, Type, TypeVar

import httpx

from .errors import (
    AuthError,
    ForbiddenError,
    InternalError,
    KairosError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)

T = TypeVar("T")

SDK_VERSION = "0.1.0"
USER_AGENT = f"kairos-sdk-python/{SDK_VERSION}"


class AsyncHttpClient:
    """Async HTTP client with automatic retry logic and error handling."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://gateway.thekairos.app/v1",
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            headers={
                "Authorization": f"Bearer {api_key}",
                "User-Agent": USER_AGENT,
            },
        )

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a GET request."""
        url = f"{self.base_url}{endpoint}"
        response = await self._request("GET", url, params=params)
        return response

    async def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a POST request."""
        url = f"{self.base_url}{endpoint}"
        response = await self._request("POST", url, data=data, json=json_data)
        return response

    async def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a PUT request."""
        url = f"{self.base_url}{endpoint}"
        response = await self._request("PUT", url, data=data, json=json_data)
        return response

    async def patch(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a PATCH request."""
        url = f"{self.base_url}{endpoint}"
        response = await self._request("PATCH", url, data=data, json=json_data)
        return response

    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make a DELETE request."""
        url = f"{self.base_url}{endpoint}"
        response = await self._request("DELETE", url)
        return response

    async def _request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        attempt: int = 0,
    ) -> Dict[str, Any]:
        """Make an HTTP request with retry logic."""
        try:
            response = await self._client.request(
                method,
                url,
                params=params,
                data=data,
                json=json,
            )
        except httpx.TimeoutException as e:
            if attempt < self.max_retries:
                await asyncio.sleep(2 ** attempt)
                return await self._request(
                    method, url, params=params, data=data, json=json, attempt=attempt + 1
                )
            raise KairosError(
                "timeout",
                f"Request timed out after {self.timeout}s",
                408,
            ) from e

        # Handle rate limiting with retry
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            if attempt < self.max_retries:
                await asyncio.sleep(retry_after)
                return await self._request(
                    method, url, params=params, data=data, json=json, attempt=attempt + 1
                )

        # Parse error responses
        if response.status_code >= 400:
            self._handle_error_response(response)

        # Parse success responses
        # Handle empty responses (e.g., 204 No Content)
        if response.status_code == 204 or not response.content:
            return {}

        try:
            return response.json()
        except json.JSONDecodeError as e:
            raise KairosError(
                "invalid_response",
                "Invalid JSON in response",
                response.status_code,
            ) from e

    def _handle_error_response(self, response: httpx.Response) -> None:
        """Parse and raise appropriate error based on status code."""
        try:
            error_data = response.json()
            error_info = error_data.get("error", {})
            code = error_info.get("code", "unknown_error")
            message = error_info.get("message", response.text)
            request_id = error_info.get("request_id")
        except (json.JSONDecodeError, ValueError):
            code = "unknown_error"
            message = response.text
            request_id = None

        status_code = response.status_code

        # Map status codes to specific exceptions
        if status_code == 401:
            raise AuthError(code, message, status_code, request_id)
        elif status_code == 403:
            raise ForbiddenError(code, message, status_code, request_id)
        elif status_code == 404:
            raise NotFoundError(code, message, status_code, request_id)
        elif status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            raise RateLimitError(message, retry_after, request_id)
        elif status_code == 400:
            raise ValidationError(code, message, status_code, request_id)
        elif status_code >= 500:
            raise InternalError(code, message, status_code, request_id)
        else:
            raise KairosError(code, message, status_code, request_id)


class SyncHttpClient:
    """Synchronous HTTP client wrapper around AsyncHttpClient."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://gateway.thekairos.app/v1",
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self._client = httpx.Client(
            timeout=httpx.Timeout(timeout),
            headers={
                "Authorization": f"Bearer {api_key}",
                "User-Agent": USER_AGENT,
            },
        )

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a GET request."""
        url = f"{self.base_url}{endpoint}"
        return self._request("GET", url, params=params)

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a POST request."""
        url = f"{self.base_url}{endpoint}"
        return self._request("POST", url, data=data, json=json_data)

    def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a PUT request."""
        url = f"{self.base_url}{endpoint}"
        return self._request("PUT", url, data=data, json=json_data)

    def patch(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a PATCH request."""
        url = f"{self.base_url}{endpoint}"
        return self._request("PATCH", url, data=data, json=json_data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make a DELETE request."""
        url = f"{self.base_url}{endpoint}"
        return self._request("DELETE", url)

    def _request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        attempt: int = 0,
    ) -> Dict[str, Any]:
        """Make an HTTP request with retry logic."""
        try:
            response = self._client.request(
                method,
                url,
                params=params,
                data=data,
                json=json,
            )
        except httpx.TimeoutException as e:
            if attempt < self.max_retries:
                import time

                time.sleep(2 ** attempt)
                return self._request(
                    method, url, params=params, data=data, json=json, attempt=attempt + 1
                )
            raise KairosError(
                "timeout",
                f"Request timed out after {self.timeout}s",
                408,
            ) from e

        # Handle rate limiting with retry
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            if attempt < self.max_retries:
                import time

                time.sleep(retry_after)
                return self._request(
                    method, url, params=params, data=data, json=json, attempt=attempt + 1
                )

        # Parse error responses
        if response.status_code >= 400:
            self._handle_error_response(response)

        # Parse success responses
        # Handle empty responses (e.g., 204 No Content)
        if response.status_code == 204 or not response.content:
            return {}

        try:
            return response.json()
        except json.JSONDecodeError as e:
            raise KairosError(
                "invalid_response",
                "Invalid JSON in response",
                response.status_code,
            ) from e

    def _handle_error_response(self, response: httpx.Response) -> None:
        """Parse and raise appropriate error based on status code."""
        try:
            error_data = response.json()
            error_info = error_data.get("error", {})
            code = error_info.get("code", "unknown_error")
            message = error_info.get("message", response.text)
            request_id = error_info.get("request_id")
        except (json.JSONDecodeError, ValueError):
            code = "unknown_error"
            message = response.text
            request_id = None

        status_code = response.status_code

        # Map status codes to specific exceptions
        if status_code == 401:
            raise AuthError(code, message, status_code, request_id)
        elif status_code == 403:
            raise ForbiddenError(code, message, status_code, request_id)
        elif status_code == 404:
            raise NotFoundError(code, message, status_code, request_id)
        elif status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            raise RateLimitError(message, retry_after, request_id)
        elif status_code == 400:
            raise ValidationError(code, message, status_code, request_id)
        elif status_code >= 500:
            raise InternalError(code, message, status_code, request_id)
        else:
            raise KairosError(code, message, status_code, request_id)
