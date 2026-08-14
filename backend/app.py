from graph import app


def run():
    print("=" * 70)
    print(
        "SECURE DOCUMENT-LEVEL RAG"
    )

    print("=" * 70)
    
    user_id = input(
        "\nEnter user ID "
        "(alice/bob/carol/david): "
    )

    query = input(
        "\nEnter your question: "
    )

    result = app.invoke({
        "query": query,
        "user_id": user_id,
        "user_groups": [],
        "documents": [],
        "answer": ""
    })


    print("\n" + "=" * 70)
    print("FINAL ANSWER")
    print("=" * 70)
    print(result["answer"])
if __name__ == "__main__":
    run()