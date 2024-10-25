from uuid import UUID

from src.core.cast_member.application.create_cast_member import (
    CreateCastMember, CreateCastMemberInput)
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import \
    InMemoryCastMemberRepository


class TestCreateCastMember:
    def test_create_cast_member_with_valid_data(self):
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repository)
        
        input = CreateCastMemberInput(name="Marilyn Monroe", type=CastMemberType.ACTOR)
        output = use_case.execute(input)
        
        assert output is not None
        assert isinstance(output.id, UUID)
        assert len(repository.cast_members) == 1
        assert repository.cast_members[0].id == output.id
        assert repository.cast_members[0].name == "Marilyn Monroe"
        assert repository.cast_members[0].type == CastMemberType.ACTOR
