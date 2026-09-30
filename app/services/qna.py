from ..gemini_client import generate_text

def answer_question_with_gemini(question: str) -> str:
    return generate_text(
        question,
        system_instruction=(
            "You are EduGenie, a helpful AI tutor. Answer accurately and clearly. "
            "Prefer simple language, examples, and short sections when useful."
        ),
        temperature=0.3, max_output_tokens=900,
    )
