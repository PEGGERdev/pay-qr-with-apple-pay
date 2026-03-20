from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class CrudRouteWrappers:
    create: list[Callable[[Callable[..., Any]], Callable[..., Any]]] = field(default_factory=list)
    read_all: list[Callable[[Callable[..., Any]], Callable[..., Any]]] = field(default_factory=list)
    read: list[Callable[[Callable[..., Any]], Callable[..., Any]]] = field(default_factory=list)
    update: list[Callable[[Callable[..., Any]], Callable[..., Any]]] = field(default_factory=list)
    delete: list[Callable[[Callable[..., Any]], Callable[..., Any]]] = field(default_factory=list)


@dataclass
class CrudRouteConfig:
    path: str | None = None
    response_model: Any = None
    status_code: int | None = None
    method: str | None = None


@dataclass
class CrudRouteConfigs:
    create: CrudRouteConfig = field(default_factory=CrudRouteConfig)
    read_all: CrudRouteConfig = field(default_factory=CrudRouteConfig)
    read: CrudRouteConfig = field(default_factory=CrudRouteConfig)
    update: CrudRouteConfig = field(default_factory=CrudRouteConfig)
    delete: CrudRouteConfig = field(default_factory=CrudRouteConfig)


@dataclass
class CrudRouteEnabled:
    create: bool = True
    read_all: bool = True
    read: bool = True
    update: bool = True
    delete: bool = True
