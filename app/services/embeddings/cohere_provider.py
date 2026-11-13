import cohere
from config import get_settings
from app.services.embeddings.base import EmbeddingProvider

class CohereEmbeddingProvider:
    MAX_BATCH_SIZE=96
    def __init__(self):
        settings=get_settings()

        self.model=settings.cohere_embedding_model
        self.dimensions=settings.cohere_embedding_dimensions

        self.client=cohere.ClientV2(
            api_key=settings.cohere_api_key.get_secret_value()
        )

    def _embed(
            self,
            texts:list[str],
            input_type:str,
    )-> list[list[str]]:
        if not texts:
            return []
        
        embeddings=[]

        for start in range(0, len(texts), self.MAX_BATCH_SIZE):
                batch = texts[start:start + self.MAX_BATCH_SIZE]

                response = self.client.embed(
                    model=self.model,
                    texts=batch,
                    input_type=input_type,
                    output_dimension=self.dimensions,
                    embedding_types=["float"],
                )

                batch_embeddings = response.embeddings.float

                if len(batch_embeddings) != len(batch):
                    raise RuntimeError(
                        "Cohere returned an unexpected number of embeddings"
                    )

                for vector in batch_embeddings:
                    if len(vector) != self.dimensions:
                        raise RuntimeError(
                            "Cohere returned an unexpected embedding dimension"
                        )

                    embeddings.append(vector)

        return embeddings

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        return self._embed(
            texts=texts,
            input_type="search_document",
        )

    def embed_query(
        self,
        text: str,
    ) -> list[float]:

        if not text.strip():
            raise ValueError("Query text cannot be empty")

        embeddings = self._embed(
            texts=[text],
            input_type="search_query",
        )

        return embeddings[0]
