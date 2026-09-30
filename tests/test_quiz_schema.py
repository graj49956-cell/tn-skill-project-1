import pytest
from pydantic import ValidationError
from app.schemas import QuizItem

def test_quiz_answer_must_be_option():
    item = QuizItem(question="Which one?", options=["A","B","C","D"], answer="B")
    assert item.answer == "B"

def test_invalid_quiz_answer_is_rejected():
    with pytest.raises(ValidationError):
        QuizItem(question="Which one?", options=["A","B","C","D"], answer="E")
