from pathlib import Path
import uuid

from pypdf import PdfReader
from langchain_text_splitters import (RecursiveCharacterTextSplitter)
from langchain_openai import (AzureOpenAIEmbeddings)
from azure.search.documents import (SearchClient)
from azure.core.credentials import (AzureKeyCredential)

from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
    AZURE_SEARCH_ENDPOINT,
    AZURE_SEARCH_API_KEY,
    AZURE_SEARCH_INDEX
)


# ------------------------------------------------
# PDF folder
# ------------------------------------------------

DOCUMENT_FOLDER = Path("documents")


# ------------------------------------------------
# Document ACL
# ------------------------------------------------

DOCUMENT_SECURITY = {
    "employee_handbook_public.pdf": ["Employees"],
    "hr_salary_policy_confidential.pdf": ["HR","Finance"],
    "project_alpha_engineering_internal.pdf": ["ProjectAlpha"]
}


# ------------------------------------------------
# Embedding model
# ------------------------------------------------

embeddings = AzureOpenAIEmbeddings(
    azure_endpoint= AZURE_OPENAI_ENDPOINT,
    api_key= AZURE_OPENAI_API_KEY,
    azure_deployment= AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
    api_version="2023-05-15"
)

# ------------------------------------------------
# Search client
# ------------------------------------------------

search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(AZURE_SEARCH_API_KEY)
)

# ------------------------------------------------
# PDF extraction
# ------------------------------------------------

def extract_pdf_text(file_path):
    reader = PdfReader(
        str(file_path)
    )

    pages = []
    for page_number, page in enumerate(reader.pages,start=1):

        text = page.extract_text()
        if text:
            pages.append({
                "page_number":
                    page_number,

                "text":
                    text
            })

    return pages

# ------------------------------------------------
# Chunking
# ------------------------------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

def create_chunks(pages):
    chunks = []
    for page in pages:
        page_chunks = splitter.split_text(page["text"])
        for chunk in page_chunks:
            chunks.append({
                "text": chunk,
                "page_number": page["page_number"]
            })

    return chunks


# ------------------------------------------------
# Process one PDF
# ------------------------------------------------

def process_pdf(file_path):
    print(
        f"\nProcessing: "
        f"{file_path.name}"
    )

    # 1. Extract
    pages = extract_pdf_text(file_path)

    # 2. Chunk
    chunks = create_chunks(
        pages
    )

    # 3. ACL
    allowed_groups = DOCUMENT_SECURITY.get(file_path.name,[])

    print(
        f"Pages: {len(pages)}"
    )

    print(
        f"Chunks: {len(chunks)}"
    )

    print(
        f"Allowed groups: "
        f"{allowed_groups}"
    )


    documents = []


    # 4. Create embeddings
    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    vectors = embeddings.embed_documents(texts)

    # 5. Build Search documents
    for i, chunk in enumerate(chunks):

        document = {
            "id":
                str(uuid.uuid4()),

            "document_id":
                file_path.stem,

            "file_name":
                file_path.name,

            "content":
                chunk["text"],

            "group_ids":
                allowed_groups,

            "content_vector":
                vectors[i]
        }

        documents.append(
            document
        )


    # 6. Upload
    if documents:
        result = search_client.upload_documents(
            documents=documents
        )

        successful = sum(
            r.succeeded
            for r in result
        )

        print(
            f"Uploaded: "
            f"{successful}/{len(documents)}"
        )


# ------------------------------------------------
# Main ingestion
# ------------------------------------------------

def main():

    if not DOCUMENT_FOLDER.exists():
        print("documents folder not found!")
        return
    
    pdf_files = list(DOCUMENT_FOLDER.glob("*.pdf"))


    if not pdf_files:
        print("No PDF files found!")
        return
    
    print(f"Found {len(pdf_files)} PDF files")

    for file_path in pdf_files:
        process_pdf(file_path)

if __name__ == "__main__":
    main()