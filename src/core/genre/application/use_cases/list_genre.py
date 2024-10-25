from dataclasses import dataclass
from uuid import UUID

from src import config
from src.core._shared.application.use_case import (ListInput, ListOutput,
                                                   ListOutputMeta)
from src.core.genre.domain.genre_repository import GenreRepository


@dataclass
class GenreOutput:
    id: UUID
    name: str
    categories: set[UUID]
    is_active: bool


class ListGenre:
    def __init__(self, repository: GenreRepository):
        self.repository = repository

    def execute(self, input: ListInput) -> ListOutput[GenreOutput]:
        genres = self.repository.list()
        
        ordered_genres = sorted(
            genres,
            key=lambda genre: getattr(genre, input.order_by)
        )
        
        page_offset = (input.current_page - 1) * config.DEFAULT_PAGINATION_SIZE
        genres_page = ordered_genres[page_offset:page_offset + config.DEFAULT_PAGINATION_SIZE]
        
        return ListOutput[GenreOutput](
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    categories=genre.categories,
                    is_active=genre.is_active,
                )
                for genre in genres_page
            ],
            meta=ListOutputMeta(
                current_page=input.current_page,
                per_page=config.DEFAULT_PAGINATION_SIZE,
                total=len(genres)
            )
        )
