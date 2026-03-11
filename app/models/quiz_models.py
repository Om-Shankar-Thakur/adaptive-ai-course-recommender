from pydantic import BaseModel


class QuizSubmission(BaseModel):
    learner_id: str
    domain: str
    topic: str
    score: float
    total_questions: int