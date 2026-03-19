from __future__ import annotations

from repositories.mongo_repository import MongoRepository


_PAYMENT_REPOSITORY: MongoRepository | None = None


def get_payment_attempt_repository() -> MongoRepository:
    global _PAYMENT_REPOSITORY
    if _PAYMENT_REPOSITORY is None:
        from models.schemas import PaymentSessionRecord

        _PAYMENT_REPOSITORY = MongoRepository(
            collection_name="payment_sessions",
            model_type=PaymentSessionRecord,
            db_name="PayQrPayments",
        )
    return _PAYMENT_REPOSITORY
