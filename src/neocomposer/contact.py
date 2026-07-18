from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Contact:
    name: str
    email: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Contact":
        return cls(
            name=data.get("name", "No name"),
            email=data.get("email", "No email"),
        )
