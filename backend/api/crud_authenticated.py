from __future__ import annotations

from typing import Any, Callable, Type, TypeVar

from fastapi import APIRouter, Body, Depends, status
from pydantic import BaseModel

from api.crud_base import GenericCrudRouter
from api.crud_types import CrudRouteConfigs, CrudRouteEnabled, CrudRouteWrappers

T = TypeVar("T", bound=BaseModel)


class AuthenticatedCrudRouter(GenericCrudRouter):
    def __init__(
        self,
        model: Type[T],
        repository,
        prefix: str,
        tags: list[str] | None = None,
        auth_dependency: Callable[..., Any] | None = None,
        id_parser: Callable[[str], Any] | None = None,
        collection_path: str = "/",
        entity_path_name: str = "entity_id",
        route_wrappers: CrudRouteWrappers | None = None,
        route_configs: CrudRouteConfigs | None = None,
        route_enabled: CrudRouteEnabled | None = None,
    ) -> None:
        super().__init__(
            model=model,
            repository=repository,
            prefix=prefix,
            tags=tags,
            id_parser=id_parser,
            collection_path=collection_path,
            entity_path_name=entity_path_name,
            route_wrappers=route_wrappers,
            route_configs=route_configs,
            route_enabled=route_enabled,
        )
        if auth_dependency is None:
            raise ValueError("AuthenticatedCrudRouter requires an auth dependency")
        self.auth_dependency = auth_dependency

    def route_dependencies(self) -> list[Any]:
        return [Depends(self.auth_dependency)]


class AuthenticatedCreateRouter(AuthenticatedCrudRouter):
    def __init__(
        self,
        model: Type[T],
        repository,
        prefix: str,
        auth_dependency: Callable[..., Any],
        create_handler: Callable[[T, dict[str, Any]], Any],
        *,
        tags: list[str] | None = None,
        response_model: Any = None,
        status_code: int = status.HTTP_200_OK,
        collection_path: str = "/",
    ) -> None:
        super().__init__(
            model=model,
            repository=repository,
            prefix=prefix,
            tags=tags,
            auth_dependency=auth_dependency,
            collection_path=collection_path,
        )
        self.create_handler = create_handler
        self.response_model = response_model
        self.create_status_code = status_code

    def include_read_all_route(self) -> bool:
        return False

    def include_read_route(self) -> bool:
        return False

    def include_update_route(self) -> bool:
        return False

    def include_delete_route(self) -> bool:
        return False

    def register_create_route(self, router: APIRouter) -> None:
        @router.post(self.collection_path, response_model=self.response_model, status_code=self.create_status_code)
        @self.handle_exceptions
        async def create(
            entity_data: dict[str, Any] = Body(...),
            current_user: dict[str, Any] = Depends(self.auth_dependency),
        ):
            return self.create_handler(self.validate_entity(entity_data), current_user)
