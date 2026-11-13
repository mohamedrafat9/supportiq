import cohere
from config import get_settings

settings = get_settings()

client = cohere.ClientV2(
    api_key=settings.cohere_api_key.get_secret_value()
)

response = client.embed(
    model="embed-v5.0-fast",
    texts=["SupportIQ is an AI-powered support platform."],
    input_type="search_document",
    embedding_types=["float"],
    output_dimension=1024,
)

print("Model request succeeded!")
print("Dimensions:", len(response.embeddings.float[0]))