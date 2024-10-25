import uuid
from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID


class CastMemberType(StrEnum):
    ACTOR = "ACTOR"
    DIRECTOR = "DIRECTOR"


@dataclass
class CastMember:
    name: str
    type: CastMemberType
    id: UUID = field(default_factory=uuid.uuid4)
    
    def __post_init__(self):
        self.validate()
        
    def validate(self):
        if not self.name:
            raise ValueError("name cannot be empty")
        
        if not self.type in CastMemberType:
            raise ValueError("type must be a valid CastMemberType")
    
    def __str__(self):
        return f"{self.name} - {self.type})"

    def __repr__(self):
        return f"<CastMember {self.name} {self.type} ({self.id})>"

    def __eq__(self, other):  # a == b -> a.__eq__(b)
        if not isinstance(other, CastMember):
            return False

        return self.id == other.id

    def update_cast_member(self, name: str, type: CastMemberType):
        self.name = name
        self.type = type
        self.validate()
