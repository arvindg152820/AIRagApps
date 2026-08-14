from langgraph.graph import (
    StateGraph,
    START,
    END
)

from state import RAGState
from security import (get_user_groups)
from search_service import (search_documents)
from llm_service import (generate_answer)


def authenticate_user(state: RAGState):
    user_id = state["user_id"]
    groups = get_user_groups(user_id)
    print(f"\nUser: {user_id}")
    print(f"Groups: {groups}")
    return {"user_groups": groups }


def retrieve_documents(state: RAGState):
    documents = search_documents(
        query=state["query"],
        user_groups=state["user_groups"], top_k=5)


    print(
        f"\nAuthorized documents "
        f"retrieved: {len(documents)}"
    )

    return {"documents": documents}


def generate_response(state: RAGState):
    answer = generate_answer(
        query=state["query"],
        documents=state["documents"]
    )

    return {
        "answer": answer
    }


# --------------------------------------
# Build LangGraph
# --------------------------------------

builder = StateGraph(RAGState)

builder.add_node(
    "authenticate_user",
    authenticate_user
)

builder.add_node(
    "retrieve_documents",
    retrieve_documents
)

builder.add_node(
    "generate_response",
    generate_response
)


builder.add_edge(
    START,
    "authenticate_user"
)

builder.add_edge(
    "authenticate_user",
    "retrieve_documents"
)

builder.add_edge(
    "retrieve_documents",
    "generate_response"
)

builder.add_edge(
    "generate_response",
    END
)


app = builder.compile()