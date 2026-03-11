from typing import Dict, Optional
from app.models.learner_profile import LearnerProfile

# In-memory learner database
learner_db: Dict[str, LearnerProfile] = {}


def get_learner(learner_id: str) -> Optional[LearnerProfile]:
    return learner_db.get(learner_id)


def save_learner(profile: LearnerProfile) -> None:
    learner_db[profile.learner_id] = profile