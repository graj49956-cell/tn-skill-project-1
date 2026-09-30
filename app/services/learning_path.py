from ..gemini_client import generate_text

def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
You are an AI tutor. The student wants to learn about: {topic}.

Suggest a structured and adaptive learning path including:
1. Beginner level: foundations and key topics.
2. Intermediate level: skills that build on the foundations.
3. Advanced level: deeper topics and practical application.
4. A sensible order of learning.
5. Useful resource types such as documentation, books, tutorials, videos,
   exercises, and project ideas. Do not invent specific links.

Keep the plan practical and student-friendly.
""".strip()
    return generate_text(
        prompt,
        system_instruction="You are EduGenie's learning-path recommendation module.",
        temperature=0.5, max_output_tokens=1800,
    )
