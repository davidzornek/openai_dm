import json

from griptape.utils.decorators import activity
from griptape.tools import BaseTool
from schema import Schema, Literal

from openai_dm.character_sheet import (
    AbilityScores,
    Character,
    SavingThrowProficiences,
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
                    ): str,
                    Literal("race", description="The race chosen by the player"): str,
                }
            ),
        }
    )
    def update_race(self, params: dict) -> Character:
        self.character_sheet.race = params["values"]["race"].lower()
        racial_bonus_dict = json.loads(params["values"]["racial_bonuses"])

        racial_ability_bonus = AbilityScores(
            strength=0,
            dexterity=0,
            constitution=0,
            intelligence=0,
            wisdom=0,
            charisma=0,
        )
        for k, v in racial_bonus_dict.items():
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
                        A json of saving throw proficiences.
                        Example: Cleric
                        {'wisdom': True, 'charisma': True}
                        """,
                    ): str,
                }
            ),
        }
    )
    def update_class(self, params: dict) -> Character:
        self.character_sheet.class_ = params["values"]["class"].lower()
        saving_throws = json.loads(params["values"]["saving_throws"])

        saving_throw_proficiences = SavingThrowProficiences()
        for x in saving_throws:
            setattr(saving_throw_proficiences, x.lower(), True)

        self.character_sheet.saving_throw_proficiencies = saving_throw_proficiences
        return self.character_sheet
