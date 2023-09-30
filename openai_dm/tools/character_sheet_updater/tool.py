import json

from griptape.utils.decorators import activity
from griptape.tools import BaseTool
from schema import Schema, Literal

from openai_dm.character_sheet import AbilityScores, Character


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
                        description="A json of racial ability score bonuses",
                    ): str,
                    Literal("race", description="The race chosen by the player"): str,
                }
            ),
        }
    )
    def update_race(self, params: dict) -> Character:
        self.character_sheet.race = params["values"]["race"]
        self.character_sheet.racial_ability_bonus = AbilityScores(
            **json.loads(params["values"]["racial_bonuses"])
        )
        self.character_sheet.apply_racial_ability_bonus()
        return self.character_sheet
