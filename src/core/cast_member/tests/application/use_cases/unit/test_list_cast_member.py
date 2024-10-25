from unittest.mock import create_autospec

import pytest

from src.core._shared.application.use_case import (ListInput, ListOutput,
                                                   ListOutputMeta)
from src.core.cast_member.application.use_cases.list_cast_member import (
    CastMemberOutput, ListCastMember)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import \
    CastMemberRepository


class TestListCastMember:
    @pytest.fixture
    def actor(self) -> CastMember:
        return CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )

    @pytest.fixture
    def director(self) -> CastMember:
        return CastMember(
            name="John Krasinski",
            type=CastMemberType.DIRECTOR,
        )

    @pytest.fixture
    def mock_empty_repository(self) -> CastMemberRepository:
        repository = create_autospec(CastMemberRepository)
        repository.list.return_value = []
        return repository

    @pytest.fixture
    def mock_populated_repository(
        self,
        actor: CastMember,
        director: CastMember,
    ) -> CastMemberRepository:
        repository = create_autospec(CastMemberRepository)
        repository.list.return_value = [
            actor,
            director,
        ]
        return repository

    def test_when_no_cast_members_then_return_empty_list(
        self,
        mock_empty_repository: CastMemberRepository,
    ) -> None:
        use_case = ListCastMember(repository=mock_empty_repository)
        response = use_case.execute(request=ListInput())

        assert response == ListOutput(data=[])

    def test_when_cast_members_exist_then_return_mapped_list(
        self,
        mock_populated_repository: CastMemberRepository,
        actor: CastMember,
        director: CastMember,
    ) -> None:
        use_case = ListCastMember(repository=mock_populated_repository)
        response = use_case.execute(request=ListInput())

        assert response == ListOutput(
            data=[
                CastMemberOutput(
                    id=actor.id,
                    name=actor.name,
                    type=actor.type,
                ),
                CastMemberOutput(
                    id=director.id,
                    name=director.name,
                    type=director.type,
                ),
            ],
            meta=ListOutputMeta(
                current_page=1,
                per_page=2,
                total=2
            )
        )
