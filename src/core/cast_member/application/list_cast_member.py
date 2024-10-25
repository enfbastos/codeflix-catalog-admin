from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import \
    CastMemberRepository


@dataclass
class ListCastMemberInput:
    ...


@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: CastMemberType


@dataclass
class ListCastMemberOutput:
    data: list[CastMemberOutput]


class ListCastMember:
    def __init__(self, repository: CastMemberRepository) -> None:
        self.repository = repository

    def execute(self, input: ListCastMemberInput) -> ListCastMemberOutput:
        cast_members = self.repository.list()
        
        return ListCastMemberOutput(
            data=[
                CastMemberOutput(
                    id=cast_member.id,
                    name=cast_member.name,
                    type=cast_member.type
                )
                for cast_member in cast_members
            ]
        )
