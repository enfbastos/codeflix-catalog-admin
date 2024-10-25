from abc import ABC, abstractmethod
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember


class CastMemberRepository(ABC):
    @abstractmethod
    def save(self, cast_member: CastMember):
        ...

    @abstractmethod
    def get_by_id(self, id: UUID) -> CastMember | None:
        ...

    @abstractmethod
    def delete(self, id: UUID) -> None:
        ...

    @abstractmethod
    def list(self) -> list[CastMember]:
        ...

    @abstractmethod
    def update(self, cast_member: CastMember) -> None:
        ...
