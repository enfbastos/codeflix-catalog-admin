from dataclasses import dataclass, field
from typing import Generic, TypeVar

from src import config

T = TypeVar("T")


@dataclass
class ListInput:
    order_by: str = "name"
    current_page: int = 1


@dataclass
class ListOutputMeta:
    current_page: int = 1
    per_page: int = config.DEFAULT_PAGINATION_SIZE
    total: int = 0


@dataclass
class ListOutput(Generic[T]):
    data: list[T]
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)
