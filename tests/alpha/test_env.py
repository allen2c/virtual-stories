import os


def test_env():
    """Test that environment variables are set correctly for testing."""
    assert os.getenv("ENVIRONMENT") == "test"
    assert os.getenv("PYTEST_IS_RUNNING") == "true"
