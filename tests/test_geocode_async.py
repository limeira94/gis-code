import pytest
from httpx import Response
from unittest.mock import AsyncMock
from tools.geocode_async import reverse_geocode


@pytest.mark.asyncio
async def test_reverse_geocode():
    
    mock_response_data = {
        "display_name": "Local test, 123, T",
    }
    
    with pytest.MonkeyPatch.context() as m:
        mock_response = Response(status_code=200, json=mock_response_data)
        m.setattr("httpx.AsyncClient.get", AsyncMock(return_value=mock_response))
        
        result = await reverse_geocode(0, 0)
        assert result == mock_response_data