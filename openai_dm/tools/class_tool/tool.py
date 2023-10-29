from attrs import define
from schema import Schema, Literal

from griptape.artifacts import TextArtifact
from griptape.utils.decorators import activity
from griptape.structures import Agent

from openai_dm.character_sheet import SavingThrowProficiencies
from openai_dm.tools import BaseSheetUpdateTool


@define(kw_only=True)
class ClassTool(BaseSheetUpdateTool):
    structure: Agent

    @activity(
        config={
            "description": "Updates the character sheet with a class selection.",
            "schema": Schema(
                {
                    Literal(
                        "class",
                        description="The class chosen by the player",
                    ): str,
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
    def update_sheet(self, params: dict) -> TextArtifact:
        super().update_sheet(params)

    def _execute_update(self, params: dict):
        self.structure.character_sheet.class_ = params["values"]["class"].lower()
        self.structure.character_sheet.hit_die = params["values"]["hit_die"]
        self.structure.character_sheet.armor_proficiencies.extend(
            [x.lower() for x in params["values"]["armor_proficiencies"]]
        )
        self.structure.character_sheet.weapon_proficiencies.extend(
            [x.lower() for x in params["values"]["weapon_proficiencies"]]
        )
        saving_throws = params["values"]["saving_throws"]

        saving_throw_proficiences = SavingThrowProficiencies()
        for x in saving_throws:
            setattr(saving_throw_proficiences, x.lower(), True)

        self.structure.character_sheet.saving_throw_proficiencies = (
            saving_throw_proficiences
        )
        self.structure.character_sheet.update_max_hp()
