import pytest
from uuid import UUID
from unittest.mock import AsyncMock, MagicMock
from fastapi import Request

from ports.inbound.http.middleware.uuid_middleware import UuidMiddleware

@pytest.mark.asyncio
async def test_uuid_middleware_dispatch():
    mock_app = MagicMock()
    
    middleware = UuidMiddleware(mock_app)

    mock_request = MagicMock(Request)
    mock_request.state = MagicMock()

    mock_call_next = AsyncMock(return_value=MagicMock(headers={}))

    response = await middleware.dispatch(mock_request, mock_call_next)

    assert hasattr(mock_request.state, "trace_id"), "O estado da requisição deveria conter um trace_id."
    trace_id = mock_request.state.trace_id
    assert isinstance(trace_id, str), "O trace_id deveria ser uma string."
    assert UUID(trace_id), "O trace_id deveria ser um UUID válido."

    assert "X-Trace-Id" in response.headers, "O cabeçalho X-Trace-Id deveria estar presente na resposta."
    assert response.headers["X-Trace-Id"] == trace_id, "O cabeçalho X-Trace-Id deveria corresponder ao trace_id gerado."

    mock_call_next.assert_awaited_once_with(mock_request)
