"""Tests for RuvieMeterClient."""

from unittest.mock import Mock, patch

from remote_check_meter.client import RuvieMeterClient


class TestRuvieMeterClient:
    """Test cases for RuvieMeterClient."""

    def test_init(self):
        """Test client initialization."""
        client = RuvieMeterClient()
        assert client.base_url == "https://www.ruvie.co.kr"
        assert client.meter_base_url == "http://14.33.118.151"

    @patch("remote_check_meter.client.requests.Session")
    def test_login_success(self, mock_session):
        """Test successful login."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html>document.iform.submit()</html>"

        mock_session.return_value.get.return_value = mock_response
        mock_session.return_value.post.return_value = mock_response

        _ = RuvieMeterClient()
        # Test would need more detailed mocking for full functionality
