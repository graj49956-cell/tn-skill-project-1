from pydantic import BaseModel, Field, field_validator

class TextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=30000)
    @field_validator("text")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Text cannot be empty.")
        return value

class TopicRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=500)
    @field_validator("topic")
    @classmethod
    def strip_topic(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Topic cannot be empty.")
        return value

class AnswerResponse(BaseModel):
    answer: str

class ExplanationResponse(BaseModel):
    topic: str
    explanation: str

class SummaryResponse(BaseModel):
    summary: str

class QuizItem(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    answer: str
    @field_validator("answer")
    @classmethod
    def answer_must_be_option(cls, value: str, info):
        options = info.data.get("options")
        if options and value not in options:
            raise ValueError("Quiz answer must exactly match one of the options.")
        return value

class QuizResponse(BaseModel):
    quiz: list[QuizItem]

class RecommendationResponse(BaseModel):
    topic: str
    recommendation: str
