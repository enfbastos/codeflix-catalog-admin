import uuid
from unittest.mock import create_autospec

import pytest

from src.core.cast_member.application.exceptions import (CastMemberNotFound,
                                                         InvalidCastMember)
from src.core.cast_member.application.update_cast_member import (
    UpdateCastMember, UpdateCastMemberInput)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import \
    CastMemberRepository


class TestUpdateCastMember:
    @pytest.fixture
    def actor(self) -> CastMember:
        return CastMember(name="Marilyn Monroe", type=CastMemberType.ACTOR)
    
    @pytest.fixture
    def mock_empty_repository(self) -> CastMemberRepository:
        repository = create_autospec(CastMemberRepository)
        repository.get_by_id.return_value = None
        return repository
    
    @pytest.fixture
    def mock_repository(self, actor: CastMember) -> CastMemberRepository:
        repository = create_autospec(CastMemberRepository, instance=True)
        repository.get_by_id.return_value = actor
        return repository
        
    def test_update_cast_member_name(
        self,
        mock_repository: CastMemberRepository,
        actor: CastMember
    ):
        use_case = UpdateCastMember(mock_repository)
        use_case.execute(
            input=UpdateCastMemberInput(
                id=actor.id,
                name="Angelina Jolie",
                type=CastMemberType.ACTOR
            )
        )
        
        assert actor.name == "Angelina Jolie"
        assert actor.type == CastMemberType.ACTOR
        mock_repository.update.assert_called_once_with(actor)
    
    def test_when_cast_member_not_found_then_raise_exception(
        self,
        mock_empty_repository: CastMemberRepository
    ) -> None:    
        use_case = UpdateCastMember(mock_empty_repository)
        
        input = UpdateCastMemberInput(
            id=uuid.uuid4(),
            name="Angelina Jolie",
            type=CastMemberType.ACTOR
        )
        
        with pytest.raises(CastMemberNotFound) as exc_info:
            use_case.execute(input)
        
        mock_empty_repository.update.assert_not_called()
        assert str(exc_info.value) == f"CastMember with {input.id} not found"
        
    def test_when_cast_member_is_updated_to_invalid_state_then_raise_exception(
        self,
        mock_repository: CastMemberRepository,
        actor: CastMember
    ) -> None:
        use_case = UpdateCastMember(mock_repository)
        input = UpdateCastMemberInput(
            id=actor.id,
            name="",
            type=""
        )
        
        with pytest.raises(InvalidCastMember) as exc_info:
            use_case.execute(input)
        
        mock_repository.update.assert_not_called()
        assert str(exc_info.value) == "name cannot be empty"
        