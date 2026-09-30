from ..gemini_client import generate_text

def summarize_text(text: str) -> str:
    prompt = (
        "Summarize the following text in simple language. Preserve important facts "
        "and relationships. Use a concise paragraph or bullet points as appropriate.\n\n"
        f"TEXT:\n{text}"
    )
    return generate_text(
        prompt,
        system_instruction="You are EduGenie's summarization module for students.",
        temperature=0.2, max_output_tokens=900,
    )
