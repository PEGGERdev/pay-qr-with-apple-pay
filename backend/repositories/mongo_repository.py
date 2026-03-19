from __future__ import annotations

import json
import os

from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import uuid4


@dataclass
class UpdateResult:
    modified_count: int


@dataclass
class DeleteResult:
    deleted_count: int


def _storage_root() -> Path:
    root = Path(os.getenv("APP_STORAGE_DIR") or Path(__file__).resolve().parents[2] / ".data")
    root.mkdir(parents=True, exist_ok=True)
    return root


class MongoRepository:
    def __init__(self, collection_name: str, model_type, db_name: str | None = None) -> None:
        self.collection_name = collection_name
        self.model_type = model_type
        self.db_name = db_name or "payQrWithApplePay"
        self.file_path = _storage_root() / f"{self.db_name}__{self.collection_name}.json"
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def _load(self) -> list[dict[str, Any]]:
        try:
            raw = self.file_path.read_text(encoding="utf-8")
            data = json.loads(raw)
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def _save(self, docs: list[dict[str, Any]]) -> None:
        self.file_path.write_text(json.dumps(docs, default=str, indent=2), encoding="utf-8")

    def _match(self, doc: dict[str, Any], query: dict[str, Any]) -> bool:
        if not query:
            return True
        if "$or" in query:
            return any(self._match(doc, clause) for clause in query["$or"])
        for key, value in query.items():
            if doc.get(key) != value:
                return False
        return True

    def insert_one(self, payload: dict[str, Any]) -> str:
        docs = self._load()
        doc = dict(payload)
        doc.setdefault("id", str(uuid4()))
        docs.append(doc)
        self._save(docs)
        return str(doc["id"])

    def create(self, entity) -> str:
        if hasattr(entity, "model_dump"):
            payload = entity.model_dump(by_alias=True)
        else:
            payload = dict(entity)
        return self.insert_one(payload)

    def find_one(self, query: dict[str, Any]) -> dict[str, Any] | None:
        for doc in self._load():
            if self._match(doc, query):
                return doc
        return None

    def find_many(self, query: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        return [doc for doc in self._load() if self._match(doc, query or {})]

    def read_all(self) -> list[dict[str, Any]]:
        return self._load()

    def read(self, entity_id: str) -> dict[str, Any] | None:
        return self.find_one({"id": entity_id})

    def update(self, entity_id: str, entity) -> UpdateResult:
        docs = self._load()
        for index, doc in enumerate(docs):
            if str(doc.get("id")) == str(entity_id):
                payload = entity.model_dump(by_alias=True) if hasattr(entity, "model_dump") else dict(entity)
                payload["id"] = str(entity_id)
                docs[index] = payload
                self._save(docs)
                return UpdateResult(modified_count=1)
        return UpdateResult(modified_count=0)

    def update_fields(self, entity_id: str, fields: dict[str, Any]) -> UpdateResult:
        docs = self._load()
        for doc in docs:
            if str(doc.get("id")) == str(entity_id):
                doc.update(fields)
                self._save(docs)
                return UpdateResult(modified_count=1)
        return UpdateResult(modified_count=0)

    def delete(self, entity_id: str) -> DeleteResult:
        docs = self._load()
        kept = [doc for doc in docs if str(doc.get("id")) != str(entity_id)]
        if len(kept) == len(docs):
            return DeleteResult(deleted_count=0)
        self._save(kept)
        return DeleteResult(deleted_count=1)

    def count_documents(self, query: dict[str, Any] | None = None) -> int:
        return len(self.find_many(query or {}))


def ping_mongo() -> bool:
    try:
        _storage_root()
        return True
    except Exception:
        return False
