from griptape.utils.decorators import activity
from griptape.tools import BaseTool
from schema import Schema, Literal

from openai_dm.character_sheet import (
    AbilityScores,
    Character,
    SavingThrowProficiencies,
)


class CharacterSheetUpdater(BaseTool):
    def __init__(self, character_sheet: Character, **kwargs):
        super().__init__(**kwargs)
        self.character_sheet = character_sheet

    @activity(
        config={
            "description": "Can be used to update the character sheet with a new race",
            "schema": Schema(
                {
                    Literal(
                        "racial_bonuses",
                        description="""
                        A json of racial ability score bonuses.
                        Example 1: Halfling
                        {"dexterity": 2}
                        Example 2: Tiefling
                        {"intelligence": 1, "charisma": 2}
                        """,
                    ): dict,
                    Literal("race", description="The race chosen by the player"): str,
                }
            ),
        }
    )
    def update_race(self, params: dict) -> Character:
        self.character_sheet.race = params["values"]["race"].lower()
        racial_bonuses = params["values"]["racial_bonuses"]

        racial_ability_bonus = AbilityScores(
            strength=0,
            dexterity=0,
            constitution=0,
            intelligence=0,
            wisdom=0,
            charisma=0,
        )
        for k, v in racial_bonuses.items():
            setattr(racial_ability_bonus, k.lower(), v)

        self.character_sheet.racial_ability_bonus = racial_ability_bonus
        self.character_sheet.apply_racial_ability_bonus()
        return self.character_sheet

    @activity(
        config={
            "description": "Can be used to update the character sheet with a new class",
            "schema": Schema(
                {
                    Literal(
                        "class",
                        description="The class chosen by the player",
                    ): str,
                    Literal(
                        "saving_throws",
                        description="""
                        A list of saving throw proficiences.
                        Example: Cleric
                        ['wisdom', 'charisma']
                        """,
                    ): list,
                    Literal(
                        "hit_die",
                        description="""Maximum value of the hit die for the chosen class""",
                    ): int,
                    Literal(
                        "armor_proficiencies",
                        description="""
                        A list of armor proficiencies for the chosen class.
                        Example: Ranger
                        ['light armor', 'medium armor', 'shields']
                        """,
                    ): list,
                    Literal(
                        "weapon_proficiencies",
                        description="""
                        A list of armor proficiencies for the chosen class.
                        Example: Warlock
                        ['simple weapons']
                        """,
                    ): list,
                }
            ),
        }
    )
    def update_class(self, params: dict) -> Character:
        self.character_sheet.class_ = params["values"]["class"].lower()
        self.character_sheet.hit_die = params["values"]["hit_die"]
        self.character_sheet.armor_proficiencies.extend(
            [x.lower() for x in params["values"]["armor_proficiencies"]]
        )
        self.character_sheet.weapon_proficiencies.extend(
            [x.lower() for x in params["values"]["weapon_proficiencies"]]
        )
        saving_throws = params["values"]["saving_throws"]

        saving_throw_proficiences = SavingThrowProficiencies()
        for x in saving_throws:
            setattr(saving_throw_proficiences, x.lower(), True)

        self.character_sheet.saving_throw_proficiencies = saving_throw_proficiences
        self.character_sheet.update_max_hp()
        return self.character_sheet

    @activity(
        config={
            "description": "Can be used to update the character sheet with new ability scores.",
            "schema": Schema(
                {
                    Literal(
                        "ability_scores",
                        description="""
                        A json of ability scores.
                        Example:
                        {"strength": 8, "dexterity": 10, "constitution": 12,
                        "intelligence": 13, "wisdom": 14, "charisma": 15}
                        """,
                    ): dict,
                }
            ),
        }
    )
    def update_ability_scores(self, params: dict) -> Character:
        ability_scores = params["values"]["ability_scores"].items()
        ability_scores = {k.lower(): v for k, v in ability_scores}

        base_ability_scores = AbilityScores(**ability_scores)

        self.character_sheet.base_ability_scores = base_ability_scores
        self.character_sheet.apply_racial_ability_bonus()
        self.character_sheet.update_max_hp()
        return self.character_sheet
