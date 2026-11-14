
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from pydantic import SecretStr

from app.services.embeddings.cohere_provider import (
    CohereEmbeddingProvider,
)


@pytest.fixture
def mock_settings():
    return SimpleNamespace(
        cohere_api_key=SecretStr("fake-api-key"),
        cohere_embedding_model="embed-v5.0-fast",
        cohere_embedding_dimensions=3,
    )


@pytest.fixture
def provider(mock_settings):
    with patch(
        "app.services.embeddings.cohere_provider.get_settings",
        return_value=mock_settings,
    ):
        with patch(
            "app.services.embeddings.cohere_provider.cohere.ClientV2"
        ) as mock_client:

            instance = CohereEmbeddingProvider()
            instance.client = mock_client.return_value

            yield instance


def make_response(vectors):
    return SimpleNamespace(
        embeddings=SimpleNamespace(float=vectors)
    )


def test_embed_documents(provider):
    provider.client.embed.return_value = make_response([
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
    ])

    result = provider.embed_documents([
        "First document",
        "Second document",
    ])

    assert result == [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
    ]

    provider.client.embed.assert_called_once_with(
        model="embed-v5.0-fast",
        texts=["First document", "Second document"],
        input_type="search_document",
        output_dimension=3,
        embedding_types=["float"],
    )


def test_embed_query(provider):
    provider.client.embed.return_value = make_response([
        [0.1, 0.2, 0.3],
    ])

    result = provider.embed_query("How can I get a refund?")

    assert result == [0.1, 0.2, 0.3]

    provider.client.embed.assert_called_once()

    call_kwargs = provider.client.embed.call_args.kwargs

    assert call_kwargs["input_type"] == "search_query"
    assert call_kwargs["texts"] == ["How can I get a refund?"]


def test_empty_documents(provider):
    result = provider.embed_documents([])

    assert result == []
    provider.client.embed.assert_not_called()


def test_empty_query(provider):
    with pytest.raises(ValueError, match="Query text cannot be empty"):
        provider.embed_query("   ")

    provider.client.embed.assert_not_called()


def test_batching(provider):
    texts = [f"Document {i}" for i in range(97)]

    provider.client.embed.side_effect = [
        make_response([[0.1, 0.2, 0.3]] * 96),
        make_response([[0.4, 0.5, 0.6]]),
    ]

    result = provider.embed_documents(texts)

    assert len(result) == 97
    assert provider.client.embed.call_count == 2

    first_batch = provider.client.embed.call_args_list[0].kwargs
    second_batch = provider.client.embed.call_args_list[1].kwargs

    assert len(first_batch["texts"]) == 96
    assert len(second_batch["texts"]) == 1


def test_unexpected_embedding_count(provider):
    provider.client.embed.return_value = make_response([
        [0.1, 0.2, 0.3],
    ])

    with pytest.raises(
        RuntimeError,
        match="unexpected number of embeddings",
    ):
        provider.embed_documents([
            "First document",
            "Second document",
        ])


def test_unexpected_embedding_dimension(provider):
    provider.client.embed.return_value = make_response([
        [0.1, 0.2],
    ])

    with pytest.raises(
        RuntimeError,
        match="unexpected embedding dimension",
    ):
        provider.embed_documents(["Test document"])
