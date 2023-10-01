from dataclasses import dataclass, field
import math
import random
from typing import Optional


@dataclass
class AbilityScores:
    strength: int = 8
    dexterity: int = 8
    constitution: int = 8
    intelligence: int = 8
    wisdom: int = 8
    charisma: int = 8


@dataclass
class SavingThrowProficiencies:
    strength: bool = False
    dexterity: bool = False
    constitution: bool = False
    intelligence: bool = False
    wisdom: bool = False
    charisma: bool = False


@dataclass
class SkillProficiencies:
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
    base_ability_scores: AbilityScores = field(default_factory=lambda: AbilityScores())
    racial_ability_bonus: AbilityScores = field(
        default_factory=lambda: AbilityScores(
            strength=0,
            dexterity=0,
            constitution=0,
            intelligence=0,
            wisdom=0,
            charisma=0,
        )
    )
    final_ability_scores: AbilityScores = field(default_factory=lambda: AbilityScores())
    saving_throw_proficiencies: SavingThrowProficiencies = field(
        default_factory=lambda: SavingThrowProficiencies()
    )
    skill_proficiencies: SkillProficiencies = field(
        default_factory=lambda: SkillProficiencies()
    )
    AC: int = 10
    speed: int = 30
    hit_die: int = 6
    hit_point_max: int = 6

    def update(self, new_values: dict):
        for k, v in new_values.items():
            if hasattr(self, k):
                setattr(self, k, v.lower())

    def apply_racial_ability_bonus(self):
        for k in self.base_ability_scores.__dataclass_fields__:
            base_score = getattr(self.base_ability_scores, k)
            racial_bonus = getattr(self.racial_ability_bonus, k)
            setattr(self.final_ability_scores, k, base_score + racial_bonus)

    def update_max_hp(self, roll_hp=True):
        constitution_modifier = (self.final_ability_scores.constitution - 10) // 2
        max_hp = self.hit_die + constitution_modifier
        if roll_hp:
            for i in range(2, self.level + 1):
                rolled_hp = random.randint(1, self.hit_die)
                max_hp += rolled_hp + constitution_modifier
        else:
            max_hp += (self.level - 1) * (
                math.ceil((self.hit_die + 1) / 2) + constitution_modifier
            )
        self.hit_point_max = max_hp
