from fastapi import APIRouter, HTTPException
from app.db.learner_store import get_learner
from app.models.response_models import ProgressSummaryResponse
from app.services.progress_analyzer import (
    determine_overall_proficiency,
    identify_skill_gaps
)

router = APIRouter()


@router.get("/progress/{learner_id}", response_model=ProgressSummaryResponse)
def get_progress(learner_id: str):
    learner = get_learner(learner_id)

    if not learner:
        raise HTTPException(status_code=404, detail="Learner not found")

    skill_gaps = identify_skill_gaps(learner.topics)
    proficiency = determine_overall_proficiency(learner.topics)

    return ProgressSummaryResponse(
        learner_id=learner_id,
        completed_topics=learner.completed_topics,
        in_progress_topics=learner.in_progress_topics,
        skill_gaps=skill_gaps,
        proficiency_level=proficiency
    )