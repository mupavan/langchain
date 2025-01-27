"""Test Anthropic API wrapper."""

from typing import Generator

from langchain.callbacks.base import CallbackManager
from langchain.llms.anthropic import Anthropic
from tests.unit_tests.callbacks.fake_callback_handler import FakeCallbackHandler


def test_anthropic_call() -> None:
    """Test valid call to anthropic."""
    llm = Anthropic(model="bare-nano-0")
    output = llm("Say foo:")
    assert isinstance(output, str)


def test_anthropic_streaming() -> None:
    """Test streaming tokens from anthropic."""
    llm = Anthropic(model="bare-nano-0")
    generator = llm.stream("I'm Pickle Rick")

    assert isinstance(generator, Generator)

    for token in generator:
        assert isinstance(token["completion"], str)


def test_anthropic_streaming_callback() -> None:
    """Test that streaming correctly invokes on_llm_new_token callback."""
    callback_handler = FakeCallbackHandler()
    callback_manager = CallbackManager([callback_handler])
    llm = Anthropic(
        model="claude-v1",
        streaming=True,
        callback_manager=callback_manager,
        verbose=True,
    )
    llm("Write me a sentence with 100 words.")
    assert callback_handler.llm_streams > 1
