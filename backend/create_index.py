from azure.search.documents.indexes import (SearchIndexClient)
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile
)

from azure.core.credentials import (AzureKeyCredential)
from backend.config import (AZURE_SEARCH_ENDPOINT,AZURE_SEARCH_API_KEY,AZURE_SEARCH_INDEX)

# ------------------------------------------------
# Search client
# ------------------------------------------------

index_client = SearchIndexClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    credential=AzureKeyCredential(AZURE_SEARCH_API_KEY)
)

# ------------------------------------------------
# Fields
# ------------------------------------------------

fields = [

    SimpleField(
        name="id",
        type=SearchFieldDataType.String,
        key=True
    ),

    SimpleField(
        name="document_id",
        type=SearchFieldDataType.String,
        filterable=True
    ),

    SearchableField(
        name="file_name",
        type=SearchFieldDataType.String,
        filterable=True
    ),

    SearchableField(
        name="content",
        type=SearchFieldDataType.String
    ),

    SearchField(
        name="group_ids",
        type=SearchFieldDataType.Collection(
            SearchFieldDataType.String
        ),
        searchable=False,
        filterable=True
    ),

    SearchField(
        name="content_vector",
        type=SearchFieldDataType.Collection(
            SearchFieldDataType.Single
        ),

        searchable=True,
        vector_search_dimensions=1536,
        vector_search_profile_name="default-profile"
    )
]


# ------------------------------------------------
# Vector configuration
# ------------------------------------------------

vector_search = VectorSearch(

    algorithms=[
        HnswAlgorithmConfiguration(
            name="hnsw"
        )
    ],

    profiles=[

        VectorSearchProfile(
            name="default-profile",
            algorithm_configuration_name="hnsw"
        )
    ]
)


# ------------------------------------------------
# Create index
# ------------------------------------------------

index = SearchIndex(
    name=AZURE_SEARCH_INDEX,
    fields=fields,
    vector_search=vector_search
)


result = index_client.create_or_update_index(index)


print(
    f"Index created successfully: "
    f"{result.name}"
)