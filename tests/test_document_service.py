import asyncio
from io import BytesIO
from uuid import uuid4
from unittest.mock import patch
from fastapi import UploadFile
import pytest
import app.services.document_storage as document_storage
from app.db.models import Workspace, Document
from app.services.document_service import upload_document_service
from sqlalchemy.exc import IntegrityError
def create_test_upload(filename: str, content: bytes) -> UploadFile:
    return UploadFile(
        filename=filename,
        file=BytesIO(content),
        headers={"content-type": "text/plain"},
    )


def test_upload_new_document(db_session, tmp_path, monkeypatch):
    monkeypatch.setattr(document_storage, "STORAGE_ROOT", tmp_path)

    workspace = Workspace(name="Test Workspace")
    db_session.add(workspace)
    db_session.flush()

    content = b"Hello SupportIQ"
    document_id = uuid4()

    file = create_test_upload("test.txt", content)

    temp_storage_path, content_hash, file_size = asyncio.run(
        document_storage.save_upload_file(
            file=file,
            workspace_name=workspace.name,
            workspace_id=workspace.id,
            document_id=document_id,
        )
    )

    temp_path = tmp_path / temp_storage_path
    assert temp_path.exists()

    document = upload_document_service(
        db=db_session,
        workspace_id=workspace.id,
        document_id=document_id,
        temp_storage_path=temp_storage_path,
        original_filename="test.txt",
        mime_type="text/plain",
        file_size_bytes=file_size,
        content_hash=content_hash,
    )

    assert document is not None
    assert document.workspace_id == workspace.id
    assert document.original_filename == "test.txt"
    assert document.content_hash == content_hash
    assert document.status == "uploaded"

    final_path = tmp_path / document.storage_path

    assert final_path.exists()
    assert final_path.read_bytes() == content
    assert not temp_path.exists()

    assert db_session.get(Document, document.id) is not None


def test_upload_duplicate_document(db_session, tmp_path, monkeypatch):
    monkeypatch.setattr(document_storage, "STORAGE_ROOT", tmp_path)

    workspace = Workspace(name="Test Workspace")
    db_session.add(workspace)
    db_session.flush()

    content = b"Hello SupportIQ"

    first_document_id = uuid4()
    first_file = create_test_upload("first.txt", content)

    first_temp_path, first_hash, first_size = asyncio.run(
        document_storage.save_upload_file(
            file=first_file,
            workspace_name=workspace.name,
            workspace_id=workspace.id,
            document_id=first_document_id,
        )
    )

    first_document = upload_document_service(
        db=db_session,
        workspace_id=workspace.id,
        document_id=first_document_id,
        temp_storage_path=first_temp_path,
        original_filename="first.txt",
        mime_type="text/plain",
        file_size_bytes=first_size,
        content_hash=first_hash,
    )

    second_document_id = uuid4()
    second_file = create_test_upload("second.txt", content)

    second_temp_path, second_hash, second_size = asyncio.run(
        document_storage.save_upload_file(
            file=second_file,
            workspace_name=workspace.name,
            workspace_id=workspace.id,
            document_id=second_document_id,
        )
    )

    second_document = upload_document_service(
        db=db_session,
        workspace_id=workspace.id,
        document_id=second_document_id,
        temp_storage_path=second_temp_path,
        original_filename="second.txt",
        mime_type="text/plain",
        file_size_bytes=second_size,
        content_hash=second_hash,
    )

    assert second_document.id == first_document.id

    documents = db_session.query(Document).filter(
        Document.workspace_id == workspace.id
    ).all()

    assert len(documents) == 1
    assert not (tmp_path / second_temp_path).exists()

    first_final_path = tmp_path / first_document.storage_path
    assert first_final_path.exists()
    assert first_final_path.read_bytes() == content


def test_same_content_in_different_workspaces(
    db_session, tmp_path, monkeypatch
):
    monkeypatch.setattr(document_storage, "STORAGE_ROOT", tmp_path)

    workspace1 = Workspace(name="Workspace 1")
    workspace2 = Workspace(name="Workspace 2")

    db_session.add_all([workspace1, workspace2])
    db_session.flush()

    content = b"Same content for both workspaces"

    documents = []

    for workspace, filename in [
        (workspace1, "file1.txt"),
        (workspace2, "file2.txt"),
    ]:
        document_id = uuid4()
        file = create_test_upload(filename, content)

        temp_storage_path, content_hash, file_size = asyncio.run(
            document_storage.save_upload_file(
                file=file,
                workspace_name=workspace.name,
                workspace_id=workspace.id,
                document_id=document_id,
            )
        )

        document = upload_document_service(
            db=db_session,
            workspace_id=workspace.id,
            document_id=document_id,
            temp_storage_path=temp_storage_path,
            original_filename=filename,
            mime_type="text/plain",
            file_size_bytes=file_size,
            content_hash=content_hash,
        )

        documents.append(document)

    assert documents[0].id != documents[1].id
    assert documents[0].content_hash == documents[1].content_hash
    assert documents[0].workspace_id == workspace1.id
    assert documents[1].workspace_id == workspace2.id

    assert len(
        db_session.query(Document).filter(
            Document.workspace_id == workspace1.id
        ).all()
    ) == 1

    assert len(
        db_session.query(Document).filter(
            Document.workspace_id == workspace2.id
        ).all()
    ) == 1


def test_upload_database_failure_cleans_up_file(
    db_session, tmp_path, monkeypatch
):
    monkeypatch.setattr(document_storage, "STORAGE_ROOT", tmp_path)

    workspace = Workspace(name="Test Workspace")
    db_session.add(workspace)
    db_session.flush()

    content = b"Database failure test"
    document_id = uuid4()

    file = create_test_upload("failure.txt", content)

    temp_storage_path, content_hash, file_size = asyncio.run(
        document_storage.save_upload_file(
            file=file,
            workspace_name=workspace.name,
            workspace_id=workspace.id,
            document_id=document_id,
        )
    )

    with patch.object(
        db_session,
        "commit",
        side_effect=Exception("Simulated database failure"),
    ):
        with pytest.raises(Exception, match="Simulated database failure"):
            upload_document_service(
                db=db_session,
                workspace_id=workspace.id,
                document_id=document_id,
                temp_storage_path=temp_storage_path,
                original_filename="failure.txt",
                mime_type="text/plain",
                file_size_bytes=file_size,
                content_hash=content_hash,
            )

    remaining_files = [path for path in tmp_path.rglob("*") if path.is_file()]
    assert remaining_files == []

    assert db_session.get(Document, document_id) is None


def test_upload_document_to_nonexistent_workspace(
    db_session, tmp_path, monkeypatch
):
    monkeypatch.setattr(document_storage, "STORAGE_ROOT", tmp_path)

    workspace_id = uuid4()
    workspace_name = "Missing Workspace"
    document_id = uuid4()
    content = b"Nonexistent workspace test"

    file = create_test_upload("test.txt", content)

    temp_storage_path, content_hash, file_size = asyncio.run(
        document_storage.save_upload_file(
            file=file,
            workspace_name=workspace_name,
            workspace_id=workspace_id,
            document_id=document_id,
        )
    )

    with pytest.raises(IntegrityError):
        upload_document_service(
            db=db_session,
            workspace_id=workspace_id,
            document_id=document_id,
            temp_storage_path=temp_storage_path,
            original_filename="test.txt",
            mime_type="text/plain",
            file_size_bytes=file_size,
            content_hash=content_hash,
        )

    remaining_files = [path for path in tmp_path.rglob("*") if path.is_file()]
    assert remaining_files == []

    assert db_session.get(Document, document_id) is None
