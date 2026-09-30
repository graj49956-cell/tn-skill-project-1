from pydantic import BaseModel
from ..gemini_client import generate_structured
from ..schemas import QuizItem

class QuizPayload(BaseModel):
    questions: list[QuizItem]

def generate_quiz(text: str) -> list[QuizItem]:
    prompt = f"""
You are a quiz generator for students.

From the passage below, create exactly 3 multiple-choice questions.
Each question must:
- test information actually present in the passage;
- have exactly 4 distinct options;
- have an answer that exactly matches one option;
- avoid trick questions and duplicates.

PASSAGE:
{text}
""".strip()
    payload = generate_structured(
        prompt, QuizPayload,
        system_instruction="Return only the requested structured quiz data.",
        temperature=0.4, max_output_tokens=1800,
    )
    if len(payload.questions) != 3:
        raise ValueError("Gemini did not return exactly 3 quiz questions.")
    return payload.questions
