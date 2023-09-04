from dataclasses import dataclass
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
    name: str = "John Doe"
    class_name: str = "Fighter"
    subclasse: Optional[str] = None
    level: int = 1
    race: str = "human"
    alignment: str = "Neutral"
    background: str = "Folk Hero"
    proficiency_bonus: int = 2
    ability_scores: AbilityScores = AbilityScores()
    saving_throw_proficiencies: SavingThrowProficiences = SavingThrowProficiences()
    skill_proficiencies: SkillProficiences = SkillProficiences()
    AC: int = 12
    speed: int = 30
    hit_point_max: int = 27
