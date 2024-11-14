import pytest
from datetime import datetime
from chatMe.core.dialogue import DialogueManager, DialogueContext

def test_create_session():
    manager = DialogueManager()
    session_id = manager.create_session("user123")
    assert session_id.startswith("user123_")
    
def test_add_message():
    manager = DialogueManager()
    session_id = manager.create_session("user123")
    
    manager.add_message(session_id, "user", "Hello")
    manager.add_message(session_id, "assistant", "Hi there!")
    
    history = manager.get_history(session_id)
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Hello"
    
def test_invalid_session():
    manager = DialogueManager()
    with pytest.raises(ValueError):
        manager.get_context("invalid_session") 