from dataclasses import dataclass
from typing import Optional


@dataclass
class CharacterSheet:
    name: Optional[str] = None
    race: Optional[str] = None
    subrace: Optional[str] = None
