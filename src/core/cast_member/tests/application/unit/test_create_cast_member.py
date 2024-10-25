from uuid import UUID

import pytest
from src.core.cast_member.application.create_cast_member import CreateCastMember, CreateCastMemberInput, CreateCastMemberOutput
from src.core.cast_member.application.exceptions import InvalidCastMember
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from unittest.mock import MagicMock


class TestCreateCastMember:
    def test_create_cast_member_with_valid(self):
        mock_repository = MagicMock(CastMemberRepository)
        use_case = CreateCastMember(repository=mock_repository)
        
        input = CreateCastMemberInput(
            name="Marilyn Monroe",
            type=CastMemberType.ACTOR
        )
        output = use_case.execute(input)
        
        assert output.id is not None
        assert isinstance(output, CreateCastMemberOutput)
        assert isinstance(output.id, UUID)
        assert mock_repository.save.called is True
    
    def test_create_cast_member_with_invalid_data(self):
        mock_repository = MagicMock(CastMemberRepository)
        use_case = CreateCastMember(repository=mock_repository)
        
        input = CreateCastMemberInput(name="", type="")
        
        with pytest.raises(InvalidCastMember, match="name cannot be empty") as exc_info:
            use_case.execute(input)
        
        assert exc_info.type is InvalidCastMember
        assert str(exc_info.value) == "name cannot be empty"
