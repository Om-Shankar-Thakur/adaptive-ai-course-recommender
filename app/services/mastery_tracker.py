def calculate_mastery(score: float) -> str:
    if score >= 80:
        return "Proficient"
    elif score >= 60:
        return "Intermediate"
    else:
        return "Beginner"