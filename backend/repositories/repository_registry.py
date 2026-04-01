from __future__ import annotations

from typing import Any, Callable

from repositories.mongo_repository import MongoRepository


_REPOSITORIES: dict[str, MongoRepository] = {}


def get_registered_repository(name: str, factory: Callable[[], MongoRepository]) -> MongoRepository:
    repository = _REPOSITORIES.get(name)
    if repository is None:
        repository = factory()
        _REPOSITORIES[name] = repository
    return repository


def reset_registered_repositories() -> None:
    _REPOSITORIES.clear()
