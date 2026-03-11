from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class QuizResponse(BaseModel):
    topic: str
    score: float
    mastery: str
    feedback: str


class CourseRecommendation(BaseModel):
    course_id: str
    course_title: Optional[str]
    course_url: Optional[str]
    difficulty: str
    xp_reward: int
    estimated_duration_hours: Optional[float]
    skills_covered: Optional[str]


class RecommendationResponse(BaseModel):
    learner_id: str
    topic: Optional[str] = None
    mastery: Optional[str] = None
    recommended_action: str
    next_difficulty: str
    recommendations: List[CourseRecommendation]
    learning_path: Optional[Dict[str, Any]] = None 

class ProgressSummaryResponse(BaseModel):
    learner_id: str
    completed_topics: List[str]
    in_progress_topics: List[str]
    skill_gaps: List[str]
    proficiency_level: str