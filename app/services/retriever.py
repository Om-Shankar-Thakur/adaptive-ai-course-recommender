from qdrant_client.models import Filter, FieldCondition, Range
from app.db.qdrant_client import client
from app.embeddings.embedder import get_embedding
from app.services.reranker import rerank_results


COLLECTION_NAME = "courses"


def retrieve_courses(
    query_text: str,
    domain: str,
    difficulty_tag: str,
    top_k: int = 10
):

    query_vector = get_embedding(query_text)

    must_conditions = [
        FieldCondition(
            key="domain",
            match={"value": domain}
        ),
        FieldCondition(
            key="difficulty_tag",
            match={"value": difficulty_tag}
        )
    ]

    search_filter = Filter(must=must_conditions)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=search_filter,
        limit=top_k
    )

    return results.points

# for testing:
# if __name__ == "__main__":
#     query = "QA student weak in selenium and xpath"

#     raw_results = retrieve_courses(
#         query_text=query,
#         domain="QA",
#         learner_score=55,
#         difficulty_tag="Intermediate"
#     )

#     reranked = rerank_results(raw_results, ["selenium", "xpath"])

#     for r in reranked:
#         print("Course:", r.payload["course_id"], "| Semantic:", r.score)

