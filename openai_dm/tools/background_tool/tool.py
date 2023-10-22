from griptape.structures import Agent
from griptape.artifacts import TextArtifact
from griptape.utils.decorators import activity
from griptape.tools import BaseTool
from schema import Schema, Literal

from openai_dm.character_sheet import SkillProficiencies


class BackgroundTool(BaseTool):
    def __init__(self, structure: Agent, **kwargs):
        super().__init__(**kwargs)
        self.structure = structure

    @activity(
        config={
            "description": "Updates the character sheet with a background selection.",
            "schema": Schema(
                {
                    Literal(
                        "background",
                        description="""The background chosen by the player""",
                    ): str,
                    Literal(
                        "skill_proficiencies",
                        description=f"Skill proficiences provided by the background.Must be a subset of {list(SkillProficiencies.__dataclass_fields__.keys())}",  # noqa: E501
                    ): list,
                }
            ),
        }
    )
    def update_background(self, params: dict) -> TextArtifact:
        if self.structure.conversation:
            self.structure.conversation.state = (
                self.structure.conversation.ConvStates.UPDATING_SHEET
            )

        self.structure.character_sheet.background = params["values"]["background"]
        skill_proficiencies = params["values"]["skill_proficiencies"]

        for x in skill_proficiencies:
            setattr(
                self.structure.character_sheet.skill_proficiencies,
                x.lower().replace(" ", "_"),
                True,
            )

        if self.structure.conversation:
            self.structure.conversation.state = (
                self.structure.conversation.ConvStates.CHANGING_NODE
            )

        return TextArtifact("The character sheet has been updated.")
