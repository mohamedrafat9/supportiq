import cohere
from config import get_settings
from app.services.embeddings.base import EmbeddingProvider
import httpx

from app.core.exceptions import (
    ProviderAuthenticationError,
    ProviderPermissionError,
    ProviderRateLimitError,
    ProviderInvalidRequestError,
    ProviderUnavailableError,
    ProviderTimeoutError,
    ProviderConnectionError,
)

class CohereEmbeddingProvider:
    MAX_BATCH_SIZE=96
    def __init__(self):
        settings=get_settings()

        self.model=settings.cohere_embedding_model
        self.dimensions=settings.cohere_embedding_dimensions

        self.client=cohere.ClientV2(
            api_key=settings.cohere_api_key.get_secret_value(),
            timeout=30,
            max_retries=2,
        )

    def _handle_provider_error(self, exc: Exception) -> None:

        if isinstance(exc, cohere.TooManyRequestsError):
            raise ProviderRateLimitError(
                "Cohere rate limit exceeded"
            ) from exc

        if isinstance(exc, (cohere.UnauthorizedError, cohere.InvalidTokenError)):
            raise ProviderAuthenticationError(
                "Cohere authentication failed"
            ) from exc

        if isinstance(exc, cohere.ForbiddenError):
            raise ProviderPermissionError(
                "Cohere permission denied"
            ) from exc

        if isinstance(
            exc,
            (
                cohere.BadRequestError,
                cohere.UnprocessableEntityError,
                cohere.NotFoundError,
            ),
        ):
            raise ProviderInvalidRequestError(
                "Cohere rejected the embedding request"
            ) from exc

        if isinstance(exc, cohere.GatewayTimeoutError):
            raise ProviderTimeoutError(
                "Cohere gateway timed out"
            ) from exc

        if isinstance(exc, httpx.TimeoutException):
            raise ProviderTimeoutError(
                "Cohere request timed out"
            ) from exc

        if isinstance(exc, httpx.ConnectError):
            raise ProviderConnectionError(
                "Could not connect to Cohere"
            ) from exc

        if isinstance(
            exc,
            (cohere.ServiceUnavailableError, cohere.InternalServerError),
        ):
            raise ProviderUnavailableError(
                "Cohere service is temporarily unavailable"
            ) from exc

    def _embed(
            self,
            texts:list[str],
            input_type:str,
    )-> list[list[float]]:
        if not texts:
            return []
        
        embeddings=[]

        for start in range(0, len(texts), self.MAX_BATCH_SIZE):
                batch = texts[start:start + self.MAX_BATCH_SIZE]
                try:
                    response = self.client.embed(
                        model=self.model,
                        texts=batch,
                        input_type=input_type,
                        output_dimension=self.dimensions,
                        embedding_types=["float"],
                    )
                except Exception as exc:
                    self._handle_provider_error(exc)
                    raise

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
