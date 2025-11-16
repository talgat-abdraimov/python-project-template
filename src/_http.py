import asyncio
from typing import Any, Awaitable, Callable

import httpx


class HttpClientError(Exception):
    """
    Base error.

    Args:
        message: The message to display.
        code: The code to display.
        details: The details to display.

    Raises:
        BaseError: The base error.
    """

    default_message = 'An error occurred'
    default_code = 'internal_server_error'
    default_details = None

    def __init__(
        self, message: str | list[str] | None = None, code: str | None = None, details: dict | None = None
    ):
        self.message = message or self.default_message
        self.code = code or self.default_code
        self.details = details or self.default_details

        super().__init__(self.message)

    def __repr__(self):
        return f'{self.__class__.__name__}(message={self.message}, code={self.code}, details={self.details})'


class HttpRetryExhaustedError(HttpClientError):
    """Raised when maximum retry attempts have been exhausted."""

    default_message = 'Maximum retry attempts exhausted'
    default_code = 'retry_exhausted'


class HttpClient:
    # Retry configuration
    MAX_RETRIES = 3
    RETRY_STATUS_CODES = {429, 500, 502, 503, 504}
    INITIAL_RETRY_DELAY = 1.0  # seconds
    MAX_RETRY_DELAY = 60.0  # seconds
    BACKOFF_MULTIPLIER = 2.0

    DEFAULT_TIMEOUT = 10.0  # seconds

    def __init__(
        self,
        *,
        base_url: str,
        max_retries: int = MAX_RETRIES,
        timeout: float | httpx.Timeout = DEFAULT_TIMEOUT,
    ) -> None:
        """
        Initialize HTTP client.

        Args:
            base_url: Base URL for all requests
            max_retries: Maximum number of retry attempts (default: 3)
            timeout: Request timeout in seconds or httpx.Timeout instance (default: 10.0)
            response_handler: Custom async function to handle responses. If not provided, uses default handler.
                            Signature: async def handler(response: httpx.Response, raise_for_status: bool) -> dict[str, Any] | None
        """
        if not isinstance(timeout, (httpx.Timeout, float, int)):
            raise ValueError('timeout must be a float, int, or httpx.Timeout instance')

        self.base_url = base_url

        self._client: httpx.AsyncClient | None = None
        self.timeout = timeout
        self.max_retries = max_retries

    @property
    def client(self) -> httpx.AsyncClient:
        """Get or create the underlying httpx AsyncClient."""

        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url, timeout=self.timeout, follow_redirects=True
            )

        return self._client

    async def close(self) -> None:
        """Close the HTTP client and release resources."""

        if self._client is not None:
            await self._client.aclose()

            self._client = None

    async def __aenter__(self) -> 'HttpClient':
        """Async context manager entry point."""
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        """Async context manager exit point."""
        await self.close()

    async def get(
        self,
        endpoint: str,
        *,
        raise_for_status: bool = True,
        response_handler: Callable[[httpx.Response, bool], Awaitable[dict[str, Any] | None]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | None:
        response = await self._perform_request(method='get', endpoint=endpoint, **kwargs)

        handler = response_handler or self.handle_response
        return await handler(response, raise_for_status)

    async def post(
        self,
        endpoint: str,
        *,
        raise_for_status: bool = True,
        response_handler: Callable[[httpx.Response, bool], Awaitable[dict[str, Any] | None]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | None:
        response = await self._perform_request(method='post', endpoint=endpoint, **kwargs)

        handler = response_handler or self.handle_response
        return await handler(response, raise_for_status)

    async def patch(
        self,
        endpoint: str,
        *,
        raise_for_status: bool = True,
        response_handler: Callable[[httpx.Response, bool], Awaitable[dict[str, Any] | None]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | None:
        response = await self._perform_request(method='patch', endpoint=endpoint, **kwargs)

        handler = response_handler or self.handle_response
        return await handler(response, raise_for_status)

    async def put(
        self,
        endpoint: str,
        *,
        raise_for_status: bool = True,
        response_handler: Callable[[httpx.Response, bool], Awaitable[dict[str, Any] | None]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | None:
        response = await self._perform_request(method='put', endpoint=endpoint, **kwargs)

        handler = response_handler or self.handle_response
        return await handler(response, raise_for_status)

    async def delete(
        self,
        endpoint: str,
        *,
        raise_for_status: bool = True,
        response_handler: Callable[[httpx.Response, bool], Awaitable[dict[str, Any] | None]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | None:
        response = await self._perform_request(method='delete', endpoint=endpoint, **kwargs)

        handler = response_handler or self.handle_response
        return await handler(response, raise_for_status)

    async def options(
        self,
        endpoint: str,
        *,
        raise_for_status: bool = True,
        response_handler: Callable[[httpx.Response, bool], Awaitable[dict[str, Any] | None]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | None:
        response = await self._perform_request(method='options', endpoint=endpoint, **kwargs)

        handler = response_handler or self.handle_response
        return await handler(response, raise_for_status)

    async def handle_response(
        self, response: httpx.Response, raise_for_status: bool = True
    ) -> dict[str, Any] | None:
        """
        Base implementation of httpx response handler.

        Args:
            response: httpx.Response object
            raise_for_status: Whether to raise an error for non-success status codes
        Returns:
            Parsed JSON response

        Raises:
            HttpClientError: If raise_for_status is True and response indicates an error else None
        """
        if not response.is_success:
            self._handle_error_response(response, raise_for_status=raise_for_status)

        if not response.content:
            return {}

        try:
            return response.json()

        except ValueError:
            # If response is successful but not JSON, return empty dict
            # Only raise if this is an actual error response
            if raise_for_status and not response.is_success:
                self._handle_error_response(response, raise_for_status=True)

            return {}

    async def _perform_request(
        self, *, method: str, endpoint: str, headers: dict[str, str] | None = None, **kwargs: dict[str, Any]
    ) -> 'httpx.Response':
        """
        Perform HTTP request with retry logic.
        Args:
            method: HTTP method (get, post, etc.)
            endpoint: API endpoint path (e.g., "pages/123")
            headers: Additional headers to include in the request
            **kwargs: Additional arguments to pass to httpx request
        Returns:
            httpx.Response object
        """
        # httpx's base_url handles URL building, just pass the endpoint
        url = endpoint

        last_response, last_exception = None, None
        for attempt in range(self.max_retries + 1):
            try:
                response = await self.client.request(method=method, url=url, headers=headers, **kwargs)
                last_response = response

                if response.is_success:
                    return response

                if not self._should_retry(response, attempt):
                    return response

                delay = self._calculate_retry_delay(attempt, retry_after=response.headers.get('Retry-After'))
                await asyncio.sleep(delay)

            except httpx.RequestError as e:
                if not self._should_retry(None, attempt):
                    last_exception = e

                    break

                delay = self._calculate_retry_delay(attempt)
                await asyncio.sleep(delay)

        if last_response is not None:
            return last_response

        if last_exception:
            raise HttpClientError(
                message=str(last_exception), code='request_error', details={'exception': repr(last_exception)}
            )

        # This should never happen but satisfy type checker
        raise HttpRetryExhaustedError(
            message='Request failed without response or exception', code='retry_exhausted'
        )

    def _should_retry(self, response: httpx.Response | None, attempt: int) -> bool:
        if attempt >= self.max_retries:
            return False

        if response is None:
            return True

        return response.status_code in self.RETRY_STATUS_CODES

    def _calculate_retry_delay(self, attempt: int, retry_after: str | None = None) -> float:
        if retry_after is not None:
            try:
                return max(float(retry_after), 0.0)

            except ValueError:
                pass

        delay = self.INITIAL_RETRY_DELAY * (self.BACKOFF_MULTIPLIER**attempt)
        return min(delay, self.MAX_RETRY_DELAY)

    def _handle_error_response(self, response: 'httpx.Response', raise_for_status: bool) -> None:
        if not raise_for_status:
            return

        try:
            data = response.json()
            message = data.get('message', 'An error occurred')
            code = data.get('code', 'unknown_error')

        except (ValueError, KeyError):
            message = response.text or 'An error occurred'
            code = 'unknown_error'

        raise HttpClientError(
            message=message,
            code=code,
            details={'status_code': response.status_code, 'raw_response': response.text},
        )
