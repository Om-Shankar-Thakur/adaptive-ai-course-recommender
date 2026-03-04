from fastapi import APIRouter, HTTPException
from app.db.learner_store import get_learner
from app.services.adaptive_engine import decide_next_action, decide_next_difficulty
from app.services.retriever import retrieve_courses
from app.services.reranker import rerank_results
from app.models.response_models import RecommendationResponse, CourseRecommendation
from app.services.prompt_builder import build_learning_path_prompt
from app.services.llm_service import generate_learning_path

router = APIRouter()


@router.get("/recommend/{learner_id}", response_model=RecommendationResponse)
def get_recommendation(learner_id: str):

    learner = get_learner(learner_id)

    if not learner:
        raise HTTPException(status_code=404, detail="Learner not found")

    if not learner.topics:
        return RecommendationResponse(
            learner_id=learner_id,
            topic=None,
            mastery=None,
            recommended_action="start_learning",
            next_difficulty="Beginner",
            recommendations=[],
            learning_path=None
        )

    weakest_topic = min(
        learner.topics.values(),
        key=lambda t: t.average_score
    )

    action = decide_next_action(weakest_topic.mastery)
    next_difficulty = decide_next_difficulty(weakest_topic.mastery)

    query_text = (
        f"{learner.domain} course for improving "
        f"{weakest_topic.topic} at {next_difficulty} level"
    )

    raw_results = retrieve_courses(
        query_text=query_text,
        domain=learner.domain,
        difficulty_tag=next_difficulty
    )

    reranked = rerank_results(raw_results, [weakest_topic.topic])

    if not reranked:
        return RecommendationResponse(
            learner_id=learner_id,
            topic=weakest_topic.topic,
            mastery=weakest_topic.mastery,
            recommended_action=action,
            next_difficulty=next_difficulty,
            recommendations=[],
            learning_path=None
        )

    top_courses = reranked[:5]

    recommendations = [
        CourseRecommendation(
            course_id=c.payload.get("course_id"),
            course_title=c.payload.get("course_title"),
            course_url=c.payload.get("course_url"),
            difficulty=c.payload.get("difficulty_tag"),
            xp_reward=c.payload.get("xp_reward"),
            estimated_duration_hours=c.payload.get("estimated_duration_hours"),
            skills_covered=c.payload.get("skills_covered"),
        )
        for c in top_courses
    ]

    learning_path = None
    overall_score = weakest_topic.average_score
    weak_skills = [weakest_topic.topic]
    try:
        llm_payload = {
        "learner_id": learner_id,
        "domain": learner.domain,
        "weak_topic": weakest_topic.topic,
        "mastery": weakest_topic.mastery,
        "overall_score": overall_score,
        "recommended_action": action,
        "next_difficulty": next_difficulty,
        "weak_skills": weak_skills,
        "recommended_courses": [
            r.model_dump() for r in recommendations
        ]
    }
        prompt = build_learning_path_prompt(llm_payload)
        learning_path = generate_learning_path(prompt)

    except Exception:
        learning_path = None

    return RecommendationResponse(
        learner_id=learner_id,
        topic=weakest_topic.topic,
        mastery=weakest_topic.mastery,
        recommended_action=action,
        next_difficulty=next_difficulty,
        recommendations=recommendations,
        learning_path=learning_path
    )
