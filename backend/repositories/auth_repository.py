from __future__ import annotations

from repositories.mongo_repository import MongoRepository


_AUTH_REPOSITORY: MongoRepository | None = None


def get_auth_user_repository() -> MongoRepository:
    global _AUTH_REPOSITORY
    if _AUTH_REPOSITORY is None:
        from models.schemas import AuthUserRecord

        _AUTH_REPOSITORY = MongoRepository(
            collection_name="users",
            model_type=AuthUserRecord,
            db_name="PayQrAuth",
        )
    return _AUTH_REPOSITORY
