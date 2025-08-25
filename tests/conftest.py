import agents
import openai
import pytest


@pytest.fixture(scope="module")
def model_name():
    """Provide the model name for testing."""
    return "gpt-4.1-nano"


@pytest.fixture(scope="module")
def openai_client():
    """Provide an async OpenAI client for testing."""
    return openai.AsyncOpenAI()


@pytest.fixture(scope="module")
def chat_model(model_name: str, openai_client: openai.AsyncOpenAI):
    """Provide a configured OpenAI responses model for testing."""
    return agents.OpenAIResponsesModel(model=model_name, openai_client=openai_client)


@pytest.fixture(scope="module")
def model_settings():
    """Provide model settings with deterministic temperature for testing."""
    return agents.ModelSettings(temperature=0.0)


@pytest.fixture(scope="module")
def agent():
    """Provide a test agent instance for testing."""
    return agents.Agent(name="Test Agent")


@pytest.fixture(scope="module")
def agents_run_config():
    """Provide run configuration with tracing disabled for testing."""
    return agents.RunConfig(tracing_disabled=True)
