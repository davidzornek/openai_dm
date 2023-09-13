from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AbilityScores:
    strength: int = 8
    dexterity: int = 8
    constitution: int = 8
    intellgience: int = 8
    wisdom: int = 8
    charisma: int = 8


@dataclass
class SavingThrowProficiences:
    strength: bool = False
    dexterity: bool = False
    constitution: bool = False
    intelligence: bool = False
    wisdom: bool = False
    charisma: bool = False


@dataclass
class SkillProficiences:
    acrobatics: bool = False
    animal_handling: bool = False
    arcana: bool = False
    athletics: bool = False
    deception: bool = False
    history: bool = False
    insight: bool = False
    intimidation: bool = False
    investigation: bool = False
    medicine: bool = False
    nature: bool = False
    perception: bool = False
    performance: bool = False
    persuasion: bool = False
    religion: bool = False
    sleight_of_hand: bool = False
    stealth: bool = False
    survival: bool = False


@dataclass
class Character:
    name: Optional[str] = None
    class_: Optional[str] = None
    subclasse: Optional[str] = None
    level: int = 1
    race: Optional[str] = None
    alignment: Optional[str] = None
    background: Optional[str] = None
    proficiency_bonus: int = 2
    ability_scores: AbilityScores = field(default_factory=lambda: AbilityScores())
    saving_throw_proficiencies: SavingThrowProficiences = field(
        default_factory=lambda: SavingThrowProficiences()
    )
    skill_proficiencies: SkillProficiences = field(
        default_factory=lambda: SkillProficiences()
    )
    AC: int = 10
    speed: int = 30
    hit_point_max: int = 6

    def update(self, new_values: dict):
        for k, v in new_values.items():
            if hasattr(self, k):
                setattr(self, k, v.lower())
