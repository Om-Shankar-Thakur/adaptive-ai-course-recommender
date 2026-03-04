import pandas as pd
from qdrant_client.models import VectorParams, Distance, PointStruct
from app.db.qdrant_client import client
from app.embeddings.embedder import get_embedding

COLLECTION_NAME = "courses"
VECTOR_SIZE = 384
BATCH_SIZE = 200  


def create_collection():
    # Modern safe way (instead of deprecated recreate_collection)
    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
    )

    print("Collection created successfully.")


def index_courses(csv_path: str):
    df = pd.read_csv(csv_path)

    points_batch = []

    for idx, row in df.iterrows():

        text_to_embed = f"""
        Title: {row['course_title']}
        Description: {row['course_description']}
        Learning Outcomes: {row['learning_outcomes']}
        Primary Skill: {row['primary_skill']}
        Skills Covered: {row['skills_covered']}
        Subtopics: {row['subtopics']}
        """

        embedding = get_embedding(text_to_embed)

        payload = {
            "course_id": row["course_id"],
            "course_title": row["course_title"],
            "domain": row["domain"],
            "level": row["level"],
            "difficulty_score": row["difficulty_score"],
            "difficulty_tag": row["difficulty_tag"],
            "estimated_duration_hours": row["estimated_duration_hours"],
            "xp_reward": row["xp_reward"],
            "recommended_for_mastery": row["recommended_for_mastery"],
            "primary_skill": row["primary_skill"],
            "skills_covered": row["skills_covered"],
            "subtopics": row["subtopics"],
            "tools_used": row["tools_used"],
            "prerequisites": row["prerequisites"],
            "course_description": row["course_description"],
            "learning_outcomes": row["learning_outcomes"],
            "rating": row["rating"],
            "course_url": row["url"],
            "score_min": row["score_min"],
            "score_max": row["score_max"]
        }

        points_batch.append(
            PointStruct(
                id=idx,
                vector=embedding,
                payload=payload
            )
        )

        # 🔥 Batch upsert every BATCH_SIZE rows
        if len(points_batch) >= BATCH_SIZE:
            client.upsert(
                collection_name=COLLECTION_NAME,
                points=points_batch
            )
            print(f"Inserted batch up to row {idx}")
            points_batch = []

    # Insert remaining rows
    if points_batch:
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points_batch
        )
        print("Inserted final batch")

    print("Indexing complete.")


if __name__ == "__main__":
    create_collection()
    index_courses("data/Online_Courses_Cleaned_Final.csv")