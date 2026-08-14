from azure.search.documents import (SearchClient)
from azure.search.documents.models import (VectorizedQuery)
from azure.core.credentials import (AzureKeyCredential)
from langchain_openai import (AzureOpenAIEmbeddings)

from .config import (
    AZURE_SEARCH_ENDPOINT,
    AZURE_SEARCH_API_KEY,
    AZURE_SEARCH_INDEX,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT
)
from .security import build_security_filter

# ------------------------------------------------
# Search client
# ------------------------------------------------

search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(
        AZURE_SEARCH_API_KEY
    )
)

# ------------------------------------------------
# Embeddings
# ------------------------------------------------

embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    azure_deployment= AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
    api_version="2025-04-01-preview"
)


# ------------------------------------------------
# Secure vector search
# ------------------------------------------------

def search_documents(query: str, user_groups: list[str], top_k: int = 5):

    # ---------------------------------------------
    # Create query embedding
    # ---------------------------------------------

    query_vector = embeddings.embed_query(query)

    # ---------------------------------------------
    # Create ACL filter
    # ---------------------------------------------

    security_filter = (build_security_filter(user_groups))
    print("\nSecurity Filter:")
    print(security_filter)

    # ---------------------------------------------
    # Vector query
    # ---------------------------------------------

    vector_query = VectorizedQuery(
        vector=query_vector,
        k_nearest_neighbors=top_k,
        fields="content_vector"
    )

    # ---------------------------------------------
    # Search
    # ---------------------------------------------

    results = search_client.search(
        search_text=query,
        vector_queries=[vector_query],
        filter=security_filter,
        top=top_k,
        select=[
            "id",
            "document_id",
            "file_name",
            "content",
            "group_ids"
        ]
    )

    documents = []
    for result in results:
        documents.append({
            "id":result.get("id"),
            "document_id": result.get("document_id"),
            "file_name": result.get("file_name"),
            "content":  result.get("content"),
            "group_ids": result.get("group_ids")
        })

    return documents