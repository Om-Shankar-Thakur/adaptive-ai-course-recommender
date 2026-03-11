from pydantic import BaseModel
from typing import Dict, List


class TopicProgress(BaseModel):
    topic: str
    attempts: int
    average_score: float
    mastery: str  


class LearnerProfile(BaseModel):
    learner_id: str
    domain: str
    topics: Dict[str, TopicProgress]  
    completed_topics: List[str]
    in_progress_topics: List[str]