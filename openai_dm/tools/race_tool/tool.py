from attrs import define
from schema import Schema, Literal

from griptape.artifacts import TextArtifact
from griptape.structures import Agent
from griptape.utils.decorators import activity

from openai_dm.character_sheet import AbilityScores
from openai_dm.tools import BaseSheetUpdateTool


@define(kw_only=True)
class RaceTool(BaseSheetUpdateTool):
    structure: Agent

    @activity(
        config={
            "description": "Updates the character sheet with a race selection.",
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
    def update_sheet(self, params: dict) -> TextArtifact:
        super().update_sheet(params)

    def _execute_update(self, params: dict):
        self.structure.character_sheet.race = params["values"]["race"].lower()
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

        self.structure.character_sheet.racial_ability_bonus = racial_ability_bonus
        self.structure.character_sheet.apply_racial_ability_bonus()
