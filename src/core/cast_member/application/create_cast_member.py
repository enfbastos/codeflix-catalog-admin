from uuid import UUID
from dataclasses import dataclass, asdict

from src.core.cast_member.application.exceptions import InvalidCastMember
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@dataclass
class CreateCastMemberInput:
    name: str
    type: CastMemberType


@dataclass
class CreateCastMemberOutput:
    id: UUID


class CreateCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    def execute(self, input: CreateCastMemberInput) -> CreateCastMemberOutput:
        try:
            cast_member = CastMember(**asdict(input))
        except ValueError as err:
            raise InvalidCastMember(err)

        self.repository.save(cast_member)
        return CreateCastMemberOutput(id=cast_member.id)
