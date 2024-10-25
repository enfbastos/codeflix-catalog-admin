from dataclasses import asdict, dataclass
from uuid import UUID

from src.core.cast_member.application.exceptions import (CastMemberNotFound,
                                                         InvalidCastMember)
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import \
    CastMemberRepository


@dataclass
class UpdateCastMemberInput:
    id: UUID
    name: str
    type: CastMemberType


class UpdateCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository
        
    def execute(self, input: UpdateCastMemberInput) -> None:
        cast_member = self.repository.get_by_id(input.id)
        
        if cast_member is None:
            raise CastMemberNotFound(f"CastMember with {input.id} not found")
        
        try:
            cast_member.update_cast_member(
                name=input.name,
                type=input.type
            )
        except ValueError as error:
            raise InvalidCastMember(error)
        
        self.repository.update(cast_member)
