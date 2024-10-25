from uuid import UUID
import uuid
import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestCastMember:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 2 required positional arguments: 'name' and 'type'"):
            CastMember()

    def test_cast_member_must_be_created_with_id_as_uuid_by_default(self):
        cast_member = CastMember(name="Marilyn Monroe", type=CastMemberType.ACTOR)
        assert isinstance(cast_member.id, UUID)
    
    def test_create_category_with_provided_values(self):
        cast_member_id = uuid.uuid4()
        cast_member = CastMember(id=cast_member_id, name="Marilyn Monroe", type=CastMemberType.ACTOR)
        assert cast_member.name == "Marilyn Monroe"
        assert cast_member.type == CastMemberType.ACTOR

    def test_cannot_create_cast_member_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            CastMember(name="", type=CastMemberType.ACTOR)
    
    def test_cannot_create_cast_member_with_invalid_type(self):
        with pytest.raises(ValueError, match="type must be a valid CastMemberType"):
            CastMember(name="Marilyn Monroe", type="")
    

class TestUpdateCastMember:
    def test_update_cast_member_with_name_and_type(self):
        cast_member = CastMember(name="Marilyn Monroe", type=CastMemberType.ACTOR)
        cast_member.update_cast_member(name="Quentin Tarantino", type=CastMemberType.DIRECTOR)
        assert cast_member.name == "Quentin Tarantino"
        assert cast_member.type == CastMemberType.DIRECTOR

    def test_update_cast_member_with_empty_name_raises_exception(self):
        cast_member = CastMember(name="Marilyn Monroe", type=CastMemberType.ACTOR)
        
        with pytest.raises(ValueError, match="name cannot be empty"):
            cast_member.update_cast_member(name="", type=cast_member.type)
    
    def test_update_cast_member_with_invalid_type_raises_exception(self):
        cast_member = CastMember(name="Marilyn Monroe", type=CastMemberType.ACTOR)
        
        with pytest.raises(ValueError, match="type must be a valid CastMemberType"):
            cast_member.update_cast_member(name="Marilyn Monroe", type="")
        

class TestEquality:
    def test_when_cast_members_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        cast_member_1 = CastMember(name="Marilyn Monroe", type=CastMemberType.ACTOR, id=common_id)
        cast_member_2 = CastMember(name="Marilyn Monroe", type=CastMemberType.ACTOR, id=common_id)

        assert cast_member_1 == cast_member_2
        
    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        cast_member = CastMember(name="Marilyn Monroe", type=CastMemberType.ACTOR, id=common_id)
        dummy = Dummy()
        dummy.id = common_id

        assert cast_member != dummy
