def calculate_skill_overlap(course_payload, weak_skills):
    if not weak_skills:
        return 0.0

    weak_skills = [skill.lower() for skill in weak_skills]

    course_skills = course_payload.get("skills_covered", "")
    course_skills = [s.strip().lower() for s in course_skills.split(",")]

    overlap = set(weak_skills).intersection(set(course_skills))

    # Normalize overlap score between 0–1
    return len(overlap) / max(len(weak_skills), 1)


def rerank_results(results, weak_skills):
    reranked = []

    for r in results:
        semantic_score = r.score  # already 0–1
        skill_score = calculate_skill_overlap(r.payload, weak_skills)

        final_score = (0.8 * semantic_score) + (0.2 * skill_score)

        reranked.append((r, final_score))

    reranked.sort(key=lambda x: x[1], reverse=True)

    return [item[0] for item in reranked]