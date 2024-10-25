import uuid

from src.core.cast_member.application.delete_cast_member import (
    DeleteCastMember, DeleteCastMemberInput)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import \
    InMemoryCastMemberRepository


class TestDeleteCastMember:
    def test_delete_cast_member_from_repository(self):
        actor = CastMember(id=uuid.uuid4(), name="Marilyn Monroe", type=CastMemberType.ACTOR)
        director = CastMember(id=uuid.uuid4(), name="Quentim Tarantino", type=CastMemberType.DIRECTOR)
        repository = InMemoryCastMemberRepository(cast_members=[actor, director])
        
        use_case = DeleteCastMember(repository=repository)
        input = DeleteCastMemberInput(id=actor.id)
        
        assert repository.get_by_id(actor.id) is not None
        output = use_case.execute(input)
        
        assert repository.get_by_id(actor.id) is None
        assert output is None
