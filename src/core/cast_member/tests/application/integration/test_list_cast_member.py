from dataclasses import asdict

import pytest

from src.core.cast_member.application.list_cast_member import (
    CastMemberOutput, ListCastMember, ListCastMemberInput,
    ListCastMemberOutput)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import \
    InMemoryCastMemberRepository


class TestListCastMember:
    @pytest.fixture
    def actor(self) -> CastMember:
        return CastMember(name="Marilyn Monroe", type=CastMemberType.ACTOR)
    
    @pytest.fixture
    def director(self) -> CastMember:
        return CastMember(name="Quentim Tarantino", type=CastMemberType.DIRECTOR)
    
    def test_when_no_cast_members_exist_then_return_empty_list(self) -> None:
        empty_repository = InMemoryCastMemberRepository()
        use_case = ListCastMember(repository=empty_repository)
        output = use_case.execute(input=ListCastMemberInput())
        assert output == ListCastMemberOutput(data=[])

    def test_when_cast_members_exist_then_return_mapped_list(self, actor: CastMember, director: CastMember) -> None:
        repository = InMemoryCastMemberRepository()
        repository.save(actor)
        repository.save(director)
        
        use_case = ListCastMember(repository=repository)
        output = use_case.execute(input=ListCastMemberInput())
        
        assert output == ListCastMemberOutput(
            data=[
                CastMemberOutput(**asdict(actor)),
                CastMemberOutput(**asdict(director))
            ]
        )
