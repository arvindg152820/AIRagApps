from langchain_openai import AzureChatOpenAI

from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_CHAT_DEPLOYMENT
)


llm = AzureChatOpenAI(
    azure_endpoint= AZURE_OPENAI_ENDPOINT,
    api_key= AZURE_OPENAI_API_KEY,
    azure_deployment= AZURE_OPENAI_CHAT_DEPLOYMENT,
    api_version="2024-10-21",
    temperature=0
)


def generate_answer(query: str,documents: list[dict]):

    if not documents:
        return (
            "I don't have access to "
            "information that can answer "
            "this question."
        )
    context = "\n\n".join(
        f"""
            Document:
            {doc["file_name"]}

            Content:
            {doc["content"]}
            """
        for doc in documents
    )

    prompt = f"""
        You are an enterprise RAG assistant.

        Answer the question using ONLY the
        authorized context below.

        Do not use your own knowledge.

        If the answer is not present in the
        authorized context, say:

        "I don't have enough authorized information
        to answer this question."

        Question:
        {query}

        Authorized Context:
        {context}
        """
    response = llm.invoke(prompt)
    return response.content