from typing import TypedDict


class RAGState(TypedDict):
    query: str
    user_id: str
    user_groups: list[str]
    documents: list[dict]
    answer: str