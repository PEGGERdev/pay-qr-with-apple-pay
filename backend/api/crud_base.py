from __future__ import annotations

from functools import wraps
from typing import Any, Callable, Dict, Type, TypeVar

from fastapi import APIRouter, Body, HTTPException, Path, Response, status
from pydantic import BaseModel, ValidationError

from api.crud_types import CrudRouteConfigs, CrudRouteEnabled, CrudRouteWrappers
from api.crud_validation import validation_error_details

T = TypeVar("T", bound=BaseModel)


class GenericCrudRouter:
    def __init__(
        self,
        model: Type[T],
        repository,
        prefix: str,
        tags: list[str] | None = None,
        id_parser: Callable[[str], Any] | None = None,
        collection_path: str = "/",
        entity_path_name: str = "entity_id",
        route_wrappers: CrudRouteWrappers | None = None,
        route_configs: CrudRouteConfigs | None = None,
        route_enabled: CrudRouteEnabled | None = None,
    ) -> None:
        self.model = model
        self.repository = repository
        self.prefix = prefix
        self.tags = tags or [prefix.strip("/")]
        self.id_parser = id_parser or self._validate_entity_id
        self.collection_path = collection_path
        self.entity_path_name = entity_path_name
        self.route_wrappers = route_wrappers or CrudRouteWrappers()
        self.route_configs = route_configs or CrudRouteConfigs()
        self.route_enabled = route_enabled or CrudRouteEnabled()

    def route_dependencies(self) -> list[Any]:
        return []

    def _validate_entity_id(self, entity_id: str) -> str:
        text = str(entity_id or "").strip()
        if not text:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
        return text

    def parse_entity_id(self, entity_id: str) -> Any:
        return self.id_parser(entity_id)

    def entity_route_path(self) -> str:
        return f"/{{{self.entity_path_name}}}"

    def include_create_route(self) -> bool:
        return self.route_enabled.create

    def include_read_all_route(self) -> bool:
        return self.route_enabled.read_all

    def include_read_route(self) -> bool:
        return self.route_enabled.read

    def include_update_route(self) -> bool:
        return self.route_enabled.update

    def include_delete_route(self) -> bool:
        return self.route_enabled.delete

    def _route_path(self, config_path: str | None, fallback: str) -> str:
        return fallback if config_path is None else config_path

    def handle_exceptions(self, func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except HTTPException:
                raise
            except Exception as exc:
                raise HTTPException(
                    status_code=getattr(exc, "status_code", 500),
                    detail={"error": str(exc), "type": exc.__class__.__name__},
                ) from exc

        return wrapper

    def validate_entity(self, entity_data: Dict[str, Any]) -> T:
        try:
            return self.model.model_validate(entity_data)
        except ValidationError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=validation_error_details(exc),
            ) from exc

    def create_entity(self, entity_data: Dict[str, Any]):
        entity = self.validate_entity(entity_data)
        entity_id = self.repository.create(entity)
        return {"id": str(entity_id)}

    def read_all_entities(self):
        return self.repository.read_all()

    def read_entity(self, entity_id: Any):
        entity = self.repository.read(entity_id)
        if not entity:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return entity

    def update_entity(self, entity_id: Any, entity_data: Dict[str, Any]):
        entity = self.validate_entity(entity_data)
        result = self.repository.update(entity_id, entity)
        if not result.modified_count:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Entity not found")
        return {"modified_count": result.modified_count}

    def delete_entity(self, entity_id: Any):
        result = self.repository.delete(entity_id)
        if result.deleted_count == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Entity not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    def register_create_route(self, router: APIRouter) -> None:
        async def create(entity_data: Dict[str, Any] = Body(...)):
            return self.create_entity(entity_data)

        wrapped = self.handle_exceptions(create)
        for route_wrapper in reversed(self.route_wrappers.create):
            wrapped = route_wrapper(wrapped)
        config = self.route_configs.create
        router.add_api_route(
            self._route_path(config.path, self.collection_path),
            wrapped,
            methods=[config.method or "POST"],
            response_model=config.response_model,
            status_code=config.status_code or status.HTTP_200_OK,
        )

    def register_read_all_route(self, router: APIRouter) -> None:
        async def read_all():
            return self.read_all_entities()

        wrapped = self.handle_exceptions(read_all)
        for route_wrapper in reversed(self.route_wrappers.read_all):
            wrapped = route_wrapper(wrapped)
        config = self.route_configs.read_all
        router.add_api_route(
            self._route_path(config.path, self.collection_path),
            wrapped,
            methods=[config.method or "GET"],
            response_model=config.response_model,
            status_code=config.status_code or status.HTTP_200_OK,
        )

    def register_read_route(self, router: APIRouter) -> None:
        async def read(entity_id: str = Path(alias=self.entity_path_name)):
            return self.read_entity(self.parse_entity_id(entity_id))

        wrapped = self.handle_exceptions(read)
        for route_wrapper in reversed(self.route_wrappers.read):
            wrapped = route_wrapper(wrapped)
        config = self.route_configs.read
        router.add_api_route(
            self._route_path(config.path, self.entity_route_path()),
            wrapped,
            methods=[config.method or "GET"],
            response_model=config.response_model,
            status_code=config.status_code or status.HTTP_200_OK,
        )

    def register_update_route(self, router: APIRouter) -> None:
        async def update(entity_id: str = Path(alias=self.entity_path_name), entity_data: Dict[str, Any] = Body(...)):
            return self.update_entity(self.parse_entity_id(entity_id), entity_data)

        wrapped = self.handle_exceptions(update)
        for route_wrapper in reversed(self.route_wrappers.update):
            wrapped = route_wrapper(wrapped)
        config = self.route_configs.update
        router.add_api_route(
            self._route_path(config.path, self.entity_route_path()),
            wrapped,
            methods=[config.method or "PUT"],
            response_model=config.response_model,
            status_code=config.status_code or status.HTTP_200_OK,
        )

    def register_delete_route(self, router: APIRouter) -> None:
        async def delete(entity_id: str = Path(alias=self.entity_path_name)):
            return self.delete_entity(self.parse_entity_id(entity_id))

        wrapped = self.handle_exceptions(delete)
        for route_wrapper in reversed(self.route_wrappers.delete):
            wrapped = route_wrapper(wrapped)
        config = self.route_configs.delete
        router.add_api_route(
            self._route_path(config.path, self.entity_route_path()),
            wrapped,
            methods=[config.method or "DELETE"],
            response_model=config.response_model,
            status_code=config.status_code or status.HTTP_200_OK,
        )

    def build(self) -> APIRouter:
        router = APIRouter(prefix=self.prefix, tags=self.tags, dependencies=self.route_dependencies())
        if self.include_create_route():
            self.register_create_route(router)
        if self.include_read_all_route():
            self.register_read_all_route(router)
        if self.include_read_route():
            self.register_read_route(router)
        if self.include_update_route():
            self.register_update_route(router)
        if self.include_delete_route():
            self.register_delete_route(router)
        return router
