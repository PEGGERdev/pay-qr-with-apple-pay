from __future__ import annotations

import os

from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from pymongo import MongoClient


@dataclass
class UpdateResult:
    modified_count: int


@dataclass
class DeleteResult:
    deleted_count: int


def mongo_url() -> str:
    return str(os.getenv("MONGO_URL") or "mongodb://localhost:27017").strip() or "mongodb://localhost:27017"


def mongo_server_selection_timeout_ms() -> int:
    return int(os.getenv("MONGO_SERVER_SELECTION_TIMEOUT_MS") or "2000")


def default_db_name() -> str:
    return str(os.getenv("MONGO_DB") or "pay_qr_with_apple_pay").strip() or "pay_qr_with_apple_pay"


def use_mock_db() -> bool:
    return str(os.getenv("USE_MOCK_DB") or "false").strip().lower() == "true"


def create_mongo_client():
    if use_mock_db():
        import mongomock

        return mongomock.MongoClient()

    return MongoClient(
        mongo_url(),
        serverSelectionTimeoutMS=mongo_server_selection_timeout_ms(),
    )


def ping_mongo() -> bool:
    client = create_mongo_client()
    try:
        client.admin.command("ping")
        return True
    finally:
        client.close()


class MongoRepository:
    def __init__(self, collection_name: str, model_type, db_name: str | None = None) -> None:
        self.collection_name = collection_name
        self.model_type = model_type
        self.db_name = str(db_name or default_db_name()).strip() or default_db_name()
        self.client = create_mongo_client()
        self.db = self.client[self.db_name]
        self.collection = self.db[collection_name]
        self.collection.create_index("id", unique=True)

    @staticmethod
    def _normalize_payload(entity) -> dict[str, Any]:
        if hasattr(entity, "model_dump"):
            payload = entity.model_dump(by_alias=True, exclude_none=True)
        else:
            payload = dict(entity)
        payload.setdefault("id", str(uuid4()))
        return payload

    def create(self, entity) -> str:
        payload = self._normalize_payload(entity)
        self.collection.insert_one(payload)
        return str(payload["id"])

    def insert_one(self, document: dict[str, Any]) -> str:
        payload = self._normalize_payload(document)
        self.collection.insert_one(payload)
        return str(payload["id"])

    def read(self, entity_id: str) -> dict[str, Any] | None:
        return self.collection.find_one({"id": str(entity_id)})

    def read_all(self) -> list[dict[str, Any]]:
        return list(self.collection.find())

    def update(self, entity_id: str, entity) -> UpdateResult:
        payload = self._normalize_payload(entity)
        payload["id"] = str(entity_id)
        result = self.collection.update_one({"id": str(entity_id)}, {"$set": payload})
        return UpdateResult(modified_count=int(result.modified_count))

    def update_fields(self, query_or_entity_id, fields: dict[str, Any], upsert: bool = False) -> UpdateResult:
        query = query_or_entity_id if isinstance(query_or_entity_id, dict) else {"id": str(query_or_entity_id)}
        result = self.collection.update_one(query, {"$set": fields}, upsert=upsert)
        return UpdateResult(modified_count=int(result.modified_count or result.upserted_id is not None))

    def delete(self, entity_id: str) -> DeleteResult:
        result = self.collection.delete_one({"id": str(entity_id)})
        return DeleteResult(deleted_count=int(result.deleted_count))

    def delete_many(self, query: dict[str, Any]) -> DeleteResult:
        result = self.collection.delete_many(query)
        return DeleteResult(deleted_count=int(result.deleted_count))

    def find_one(self, query: dict[str, Any], projection: dict[str, int] | None = None):
        return self.collection.find_one(query, projection)

    def find_many(self, query: dict[str, Any] | None = None, projection: dict[str, int] | None = None, limit: int = 0):
        cursor = self.collection.find(query or {}, projection)
        if limit and limit > 0:
            cursor = cursor.limit(int(limit))
        return list(cursor)

    def count_documents(self, query: dict[str, Any] | None = None, limit: int = 0) -> int:
        if limit and limit > 0:
            return self.collection.count_documents(query or {}, limit=int(limit))
        return self.collection.count_documents(query or {})
