"""
Tests for the logging configuration module.
Verifies logger setup, structured JSON formatting, and logger retrieval functions.
"""

import sys
import json
import logging
import os
from pathlib import Path
from io import StringIO
import pytest

from utils.logging import StructuredJsonFormatter, get_logger, setup_logging


@pytest.fixture(autouse=True)
def manage_logging_state():
    """Fixture to save and restore logging state for each test."""
    # Add a dummy handler to ensure the handler removal loop in setUp
    # and handler addition loop in tearDown are always entered.
    dummy_handler_for_setup = logging.NullHandler()
    logging.getLogger().addHandler(dummy_handler_for_setup)

    original_handlers = logging.getLogger().handlers.copy()
    original_level = logging.getLogger().level

    # Reset root logger for clean test environment
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    yield

    # Restore original root logger handlers and level
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    for handler in original_handlers:
        root_logger.addHandler(handler)

    root_logger.setLevel(original_level)

    # Clean up any file handlers created during tests
    for handler in logging.getLogger().handlers[:]:
        if isinstance(handler, logging.FileHandler):
            handler.close()
            logging.getLogger().removeHandler(handler)


def test_structured_json_formatter():
    """Test that JSON formatter produces correctly structured output."""
    formatter = StructuredJsonFormatter()

    # Create a log record
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test_path",
        lineno=42,
        msg="Test message",
        args=(),
        exc_info=None,
    )

    # Format the record
    formatted = formatter.format(record)

    # Parse the JSON result
    log_entry = json.loads(formatted)

    # Check the formatted output
    assert log_entry["level"] == "INFO"
    assert log_entry["name"] == "test_logger"
    assert log_entry["message"] == "Test message"
    assert "timestamp" in log_entry


def test_setup_logging_default(tmp_path):
    """Test default logging setup configuration."""
    log_file = tmp_path / "test.log"
    setup_logging(log_file=str(log_file))

    # Check that the root logger has the expected level
    assert logging.getLogger().level == logging.INFO

    # Check handlers were created
    root_handlers = logging.getLogger().handlers
    assert len(root_handlers) == 2  # Console and file handler

    # Verify handlers
    handler_types = [type(h) for h in root_handlers]
    assert logging.StreamHandler in handler_types
    assert logging.FileHandler in handler_types

    # Verify log file was created
    assert log_file.exists()


def test_setup_logging_custom_level(tmp_path):
    """Test logging setup with custom log level."""
    log_file = tmp_path / "debug.log"
    setup_logging(log_level="DEBUG", log_file=str(log_file))

    # Check that the root logger has the expected level
    assert logging.getLogger().level == logging.DEBUG


def test_setup_logging_json_format(tmp_path):
    """Test logging setup with JSON formatting enabled."""
    log_file = tmp_path / "json.log"
    setup_logging(json_format=True, log_file=str(log_file))

    # Check that handlers use JSON formatter
    for handler in logging.getLogger().handlers:
        assert isinstance(handler.formatter, StructuredJsonFormatter)


def test_get_logger():
    """Test retrieving a logger by name."""
    logger = get_logger("test.namespace")
    assert logger.name == "test.namespace"


def test_logging_output():
    """Test that log messages are formatted as expected."""
    # Setup logging with StringIO to capture output
    string_io = StringIO()
    handler = logging.StreamHandler(string_io)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    test_logger = logging.getLogger("test.output")
    # Ensure logger is clean for this specific test
    for h in test_logger.handlers[:]:
        test_logger.removeHandler(h)
    test_logger.setLevel(logging.INFO)
    test_logger.addHandler(handler)

    # Log a test message
    test_message = "This is a test log message"
    test_logger.info(test_message)

    # Check the output
    output = string_io.getvalue().strip()
    assert output == f"INFO - {test_message}"
    # Clean up handler for this specific logger
    test_logger.removeHandler(handler)


def test_structured_json_formatter_with_exception():
    """Test that exception information is included in JSON-formatted logs."""
    formatter = StructuredJsonFormatter()

    # Create an exception
    try:
        raise ValueError("Test exception")
    except ValueError:
        exc_info = sys.exc_info()

    # Create a log record with exception info
    record = logging.LogRecord(
        name="test_logger",
        level=logging.ERROR,
        pathname="test_path",
        lineno=42,
        msg="Exception occurred",
        args=(),
        exc_info=exc_info,
    )

    # Format the record
    formatted = formatter.format(record)

    # Parse the JSON result
    log_entry = json.loads(formatted)

    # Check exception info was included
    assert "exception" in log_entry
    assert "ValueError: Test exception" in log_entry["exception"]


def test_structured_json_formatter_with_extra_fields():
    """Test that extra fields are included in JSON-formatted logs."""
    formatter = StructuredJsonFormatter()

    # Create a log record with extra attribute
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test_path",
        lineno=42,
        msg="Test message with extra",
        args=(),
        exc_info=None,
    )
    # Add extra fields directly to record.__dict__
    record.request_id = "123456"
    record.user_id = "user-789"

    # Format the record
    formatted = formatter.format(record)

    # Parse the JSON result
    log_entry = json.loads(formatted)

    # Check extra fields were included
    assert log_entry["request_id"] == "123456"
    assert log_entry["user_id"] == "user-789"


def test_setup_logging_default_file_path(tmp_path):
    """Test that default log directory and file are created when not specified."""
    original_dir = os.getcwd()
    os.chdir(tmp_path)  # Change to temp directory for this test

    try:
        # Call setup_logging with default log_file (None)
        setup_logging(log_file=None)

        # Check logs directory was created
        logs_dir = Path("logs")
        assert logs_dir.exists()
        assert logs_dir.is_dir()

        # Check default log file was created
        default_log_file = logs_dir / "app.log"
        assert default_log_file.exists()
    finally:
        os.chdir(original_dir)  # Return to original directory


def test_setup_logging_creates_parent_dirs(tmp_path):
    """Test that parent directories are created for log file if they don't exist."""
    # Create a multi-level path that doesn't exist yet
    nested_log_path = tmp_path / "nested" / "dirs" / "logs" / "test.log"

    # This should create all parent directories
    setup_logging(log_file=str(nested_log_path))

    # Verify directories were created
    assert nested_log_path.parent.exists()
    assert nested_log_path.exists()


def test_third_party_logger_levels(tmp_path):
    """Test that third-party loggers are set to WARNING level to reduce verbosity."""
    log_file = tmp_path / "third_party.log"
    setup_logging(log_file=str(log_file))

    # Verify third-party logger levels
    assert logging.getLogger("sqlalchemy").level == logging.WARNING
    assert logging.getLogger("sqlalchemy.engine").level == logging.WARNING
    assert logging.getLogger("uvicorn").level == logging.WARNING
    assert logging.getLogger("uvicorn.access").level == logging.WARNING
    assert logging.getLogger("fastapi").level == logging.WARNING


def test_structured_json_formatter_with_record_extra():
    """Test handling of nested 'extra' attribute in log records."""
    formatter = StructuredJsonFormatter()

    # Create a log record
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test_path",
        lineno=42,
        msg="Test message with extra attribute",
        args=(),
        exc_info=None,
    )

    # Add an 'extra' attribute to the record
    record.extra = {"transaction_id": "txn-123", "correlation_id": "corr-456"}

    # Format the record
    formatted = formatter.format(record)

    # Parse the JSON result
    log_entry = json.loads(formatted)

    # Check that fields from record.extra were included
    assert log_entry["transaction_id"] == "txn-123"
    assert log_entry["correlation_id"] == "corr-456"


def test_setup_logging_removes_existing_handlers(tmp_path):
    """Test that setup_logging removes existing handlers before adding new ones."""
    log_file = tmp_path / "handlers.log"

    # Add a test handler to the root logger before setup_logging
    root_logger = logging.getLogger()
    # Ensure the test handler is added to a clean slate for this test's purpose
    # The autouse fixture will clean up handlers *after* this test,
    # but we want to ensure no handlers from *previous* tests interfere here.
    for handler in root_logger.handlers[:]:
        if (
            handler is not logging.getLogger().handlers[0]
        ):  # Keep the dummy one from fixture
            root_logger.removeHandler(handler)

    test_handler = logging.StreamHandler(StringIO())
    root_logger.addHandler(test_handler)

    # Count handlers before setup_logging (should include dummy + test_handler)
    # The dummy handler is added by the fixture.
    assert test_handler in root_logger.handlers
    # Allow for the fixture's dummy handler
    assert len(root_logger.handlers) >= 2

    # Call setup_logging
    setup_logging(log_file=str(log_file))

    # Verify the test handler was removed
    assert test_handler not in root_logger.handlers

    # Should have exactly 2 handlers (console and file)
    assert len(root_logger.handlers) == 2


def test_remove_all_handlers_from_logger():
    """Test that all handlers are removed from a logger using the handler removal loop."""
    logger = logging.getLogger("test.remove.handlers")
    # Add multiple handlers
    handler1 = logging.StreamHandler(StringIO())
    handler2 = logging.StreamHandler(StringIO())
    logger.addHandler(handler1)
    logger.addHandler(handler2)
    assert len(logger.handlers) >= 2  # Ensure handlers are present

    # Remove all handlers using the tested loop
    for h in logger.handlers[:]:
        logger.removeHandler(h)

    # Assert all handlers are removed
    assert len(logger.handlers) == 0
