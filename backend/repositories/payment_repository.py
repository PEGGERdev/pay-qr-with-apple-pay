from __future__ import annotations

from repositories.mongo_repository import MongoRepository
from repositories.repository_registry import get_registered_repository


def get_payment_attempt_repository() -> MongoRepository:
    def build_repository() -> MongoRepository:
        from models.schemas import PaymentSessionRecord

        return MongoRepository(
            collection_name="payment_sessions",
            model_type=PaymentSessionRecord,
            db_name="PayQrPayments",
        )
    return get_registered_repository("payments.sessions", build_repository)
