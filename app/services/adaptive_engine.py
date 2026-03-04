LEVELS = ["Beginner", "Intermediate", "Advanced"]

MASTERY_TO_LEVEL = {
    "Beginner": "Beginner",
    "Intermediate": "Intermediate",
    "Proficient": "Advanced"
}


def decide_next_action(mastery: str) -> str:
    if mastery == "Beginner":
        return "remedial"
    elif mastery == "Proficient":
        return "advance"
    return "continue"


def decide_next_difficulty(mastery: str) -> str:
    """
    Map mastery directly to next difficulty.
    """
    return MASTERY_TO_LEVEL.get(mastery, "Beginner")