def build_learning_path_prompt(payload: dict) -> str:

    courses_text = ""

    for idx, course in enumerate(payload["recommended_courses"], 1):
        courses_text += f"""
Course {idx}:
- Course ID: {course['course_id']}
- Title: {course.get('course_title')}
- Difficulty: {course.get('difficulty')}
- Estimated Duration (Hours): {course.get('estimated_duration_hours')}
- Skills Covered: {course.get('skills_covered')}
- Subtopics: {course.get('subtopics')}
- Tools Used: {course.get('tools_used')}
- Prerequisites: {course.get('prerequisites')}
- XP Reward: {course.get('xp_reward')}
"""

    return f"""
You are an expert AI learning architect.

Your task is to generate a highly practical, logically sequenced, 5-week adaptive learning roadmap.

STRICT RULES:
- Return ONLY valid JSON.
- Do NOT return markdown.
- Do NOT include explanations outside JSON.
- Use ONLY the courses provided.
- Do NOT invent course titles or skills.
- Sequence courses logically based on difficulty and prerequisites.
- Each week must build upon the previous week.
- Adjust complexity according to mastery level and score.
- Make tasks implementation-focused (projects, coding, automation, practice).
- XP target should scale progressively.

RETURN THIS EXACT JSON STRUCTURE:

{{
  "weeks": [
    {{
      "week": 1,
      "course_id": "",
      "course_title": "",
      "objective": "",
      "focus_topics": [],
      "practical_tasks": [],
      "tools_to_use": [],
      "estimated_hours": 0,
      "xp_target": 0
    }}
  ],
  "skill_progression_summary": "",
  "key_competencies_gained": [],
  "final_motivation": ""
}}

--------------------------------------------------
LEARNER PROFILE
--------------------------------------------------
Domain: {payload['domain']}
Current Mastery Level: {payload['mastery']}
Overall Score: {payload['overall_score']}
Recommended Action: {payload['recommended_action']}
Next Difficulty Level: {payload['next_difficulty']}
Weak Skills: {", ".join(payload.get('weak_skills', []))}

--------------------------------------------------
RECOMMENDED COURSES
--------------------------------------------------
{courses_text}

Generate the adaptive roadmap now.
"""