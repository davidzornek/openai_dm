from griptape.structures import Agent
from griptape.artifacts import TextArtifact
from griptape.utils.decorators import activity
from griptape.tools import BaseTool
from schema import Schema, Literal

from openai_dm.character_sheet import SavingThrowProficiencies


class ClassTool(BaseTool):
    def __init__(self, structure: Agent, **kwargs):
        super().__init__(**kwargs)
        self.structure = structure

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
    def update_class(self, params: dict) -> TextArtifact:
        if self.structure.conversation:
            self.structure.conversation.state = (
                self.structure.conversation.ConvStates.UPDATING_SHEET
            )

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

        if self.structure.conversation:
            self.structure.conversation.state = (
                self.structure.conversation.ConvStates.CHANGING_NODE
            )

        return TextArtifact("The character sheet has been updated.")
