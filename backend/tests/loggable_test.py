import datetime
import pytest
from unittest.mock import patch

from shared.loggable import Loggable

@pytest.fixture
def loggable_instance():
    return Loggable(prefix="TestPrefix")


def test_logger_format_message_with_trace_id():
    """Teste para o formato da mensagem com trace_id."""
    logger = Loggable.Logger(prefix="TestPrefix")
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime.datetime(2025, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
        mock_datetime.now.return_value.isoformat.return_value = "2025-01-01T12:00:00+00:00"
        message = logger._format_message("info", "This is a test message", trace_id="trace-123")
        expected = "2025-01-01T12:00:00+00:00 TestPrefix info: [trace-123] This is a test message"
        assert message == expected

def test_logger_format_message_without_trace_id():
    logger = Loggable.Logger(prefix="TestPrefix")
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime.datetime(2025, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
        mock_datetime.now.return_value.isoformat.return_value = "2025-01-01T12:00:00+00:00"
        message = logger._format_message("info", "This is a test message")
        expected = "2025-01-01T12:00:00+00:00 TestPrefix info:  This is a test message"
        assert message == expected

def test_logger_info(capsys):
    logger = Loggable.Logger(prefix="TestPrefix")
    logger.info("Test info message", trace_id="trace-123")
    captured = capsys.readouterr()
    assert "TestPrefix info: [trace-123] Test info message" in captured.out
    assert captured.err == ""


def test_logger_error(capsys):
    logger = Loggable.Logger(prefix="TestPrefix")
    logger.error("Test error message", trace_id="trace-123")
    captured = capsys.readouterr()
    assert "TestPrefix error: [trace-123] Test error message" in captured.err
    assert captured.out == ""
