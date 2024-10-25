from dataclasses import asdict
from unittest.mock import create_autospec

import pytest

from src.core.cast_member.application.list_cast_member import (
    CastMemberOutput, ListCastMember, ListCastMemberInput,
    ListCastMemberOutput)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import \
    CastMemberRepository


class TestListCastMember:
    @pytest.fixture
    def actor(self) -> CastMember:
        return CastMember(name="Marilyn Monroe", type=CastMemberType.ACTOR)
    
    @pytest.fixture
    def director(self) -> CastMember:
        return CastMember(name="Quentin Tarantino", type=CastMemberType.DIRECTOR)

    @pytest.fixture
    def mock_empty_repository(self) -> CastMemberRepository:
        repository = create_autospec(CastMemberRepository)
        repository.list.return_value = []
        return repository
    
    @pytest.fixture
    def mock_populate_repository(self, actor: CastMember, director: CastMember) -> CastMemberRepository:
        repository = create_autospec(CastMemberRepository)
        repository.list.return_value = [actor, director]
        return repository
    
    def test_when_no_cast_members_then_return_empty_list(self, mock_empty_repository: CastMemberRepository) -> None:
        use_case = ListCastMember(repository=mock_empty_repository)
        output = use_case.execute(input=ListCastMemberInput())
        assert output == ListCastMemberOutput(data=[])

    def test_when_cast_members_exist_then_return_mapped_list(self, mock_populate_repository: CastMemberRepository, actor: CastMember, director: CastMember) -> None:
        use_case = ListCastMember(repository=mock_populate_repository)
        output = use_case.execute(input=ListCastMemberInput())
        assert output == ListCastMemberOutput(
            data=[
                CastMemberOutput(**asdict(actor)),
                CastMemberOutput(**asdict(director))
            ]
        )
