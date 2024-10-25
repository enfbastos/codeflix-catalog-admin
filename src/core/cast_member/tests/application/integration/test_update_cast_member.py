from src.core.cast_member.application.update_cast_member import (
    UpdateCastMember, UpdateCastMemberInput)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import \
    InMemoryCastMemberRepository


class TestUpdateCastMember:
    def test_update_cast_member_with_provided_values(self):
        cast_member = CastMember(name="Marilyn Monroe", type=CastMemberType.ACTOR)
        repository = InMemoryCastMemberRepository()
        repository.save(cast_member)
        
        use_case = UpdateCastMember(repository=repository)
        input = UpdateCastMemberInput(
            id=cast_member.id,
            name="Quentim Tarantino",
            type=CastMemberType.DIRECTOR
        )
        output = use_case.execute(input)
        
        updated_cast_member = repository.get_by_id(cast_member.id)
        assert output is None
        assert updated_cast_member.name == "Quentim Tarantino"
        assert updated_cast_member.type == CastMemberType.DIRECTOR
