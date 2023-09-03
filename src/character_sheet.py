from dataclasses import dataclass
from typing import Optional


@dataclass
class Character:
    name: str = "John Doe"
    char_class: str = "Fighter"
    subclasse: Optional[str] = None
    level: int = 1
    race: str = "human"
    alignment: str = "Neutral"
    background: str = "Folk Hero"
    proficiency_bonus: str = 1
    ability_scores: dict = {
        "strength": 8,
        "dexterity": 14,
        "constitution": 13,
        "intelligence": 18,
        "wisdom": 12,
        "charisma": 10,
    }
    saving_throw_proficiencies: dict = {
        "strength": False,
        "dexterity": False,
        "constitution": False,
        "intelligence": False,
        "wisdom": False,
        "charisma": False,
    }
    skill_proficiencies: dict = {
        "acrobatics": False,
        "animal_handling": False,
        "arcana": True,
        "athletics": False,
        "deception": False,
        "history": True,
        "insight": False,
        "intimidation": False,
        "investigation": True,
        "medicine": True,
        "nature": False,
        "perception": True,
        "performance": False,
        "persuasion": False,
        "religion": True,
        "sleight_of_hand": True,
        "stealth": False,
        "survival": False,
    }
    AC: int = 12
    speed: int = 30
    hit_point_max: int = 27
