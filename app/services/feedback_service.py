def generate_feedback(score: float) -> str:
    if score >= 80:
        return "Great work. You have strong understanding of this topic."
    elif score >= 60:
        return "Good attempt. Review weak areas and practice more."
    else:
        return "You need remedial practice on this topic."