from __future__ import annotations

from repositories.mongo_repository import MongoRepository
from repositories.repository_registry import get_registered_repository


def get_auth_user_repository() -> MongoRepository:
    def build_repository() -> MongoRepository:
        from models.schemas import AuthUserRecord

        return MongoRepository(
            collection_name="users",
            model_type=AuthUserRecord,
            db_name="PayQrAuth",
        )
    return get_registered_repository("auth.users", build_repository)
