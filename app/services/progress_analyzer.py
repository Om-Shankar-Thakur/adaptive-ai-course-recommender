def determine_overall_proficiency(topics: dict) -> str:
    """
    Determine overall learner level based on average mastery level.
    """

    if not topics:
        return "Beginner"

    mastery_map = {
        "Beginner": 1,
        "Intermediate": 2,
        "Proficient": 3,
        "Expert": 3
    }

    numeric_levels = []

    for topic in topics.values():
        numeric_levels.append(
            mastery_map.get(topic.mastery, 1)
        )

    avg_level = sum(numeric_levels) / len(numeric_levels)

    if avg_level < 1.5:
        return "Beginner"
    elif avg_level < 2.5:
        return "Intermediate"
    else:
        return "Proficient"


def identify_skill_gaps(topics: dict):
    """
    Skill gaps = topics where mastery is Beginner
    """

    return [
        t.topic
        for t in topics.values()
        if t.mastery == "Beginner"
    ]