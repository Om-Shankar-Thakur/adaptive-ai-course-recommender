from fastapi import APIRouter
from app.models.quiz_models import QuizSubmission
from app.models.response_models import QuizResponse
from app.models.learner_profile import LearnerProfile, TopicProgress
from app.services.mastery_tracker import calculate_mastery
from app.services.feedback_service import generate_feedback
from app.db.learner_store import get_learner, save_learner

router = APIRouter()


@router.post("/submit-quiz", response_model=QuizResponse)
def submit_quiz(quiz: QuizSubmission):
    learner = get_learner(quiz.learner_id)

    # If learner does not exist, create new profile
    if not learner:
        learner = LearnerProfile(
            learner_id=quiz.learner_id,
            domain=quiz.domain,
            topics={},
            completed_topics=[],
            in_progress_topics=[]
        )

    # Get existing topic progress or create new
    topic_progress = learner.topics.get(quiz.topic)

    if topic_progress:
        new_attempts = topic_progress.attempts + 1
        new_avg_score = (
            (topic_progress.average_score * topic_progress.attempts + quiz.score)
            / new_attempts
        )
    else:
        new_attempts = 1
        new_avg_score = quiz.score

    mastery = calculate_mastery(new_avg_score)

    updated_topic = TopicProgress(
        topic=quiz.topic,
        attempts=new_attempts,
        average_score=new_avg_score,
        mastery=mastery
    )

    learner.topics[quiz.topic] = updated_topic

    # Update progress lists
    if mastery == "Proficient":
        if quiz.topic not in learner.completed_topics:
            learner.completed_topics.append(quiz.topic)
        if quiz.topic in learner.in_progress_topics:
            learner.in_progress_topics.remove(quiz.topic)
    else:
        if quiz.topic not in learner.in_progress_topics:
            learner.in_progress_topics.append(quiz.topic)

    save_learner(learner)

    feedback = generate_feedback(quiz.score)

    return {
        "topic": quiz.topic,
        "score": quiz.score,
        "mastery": mastery,
        "feedback": feedback
    }