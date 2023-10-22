from griptape.structures import Agent
from griptape.artifacts import TextArtifact
from griptape.utils.decorators import activity
from griptape.tools import BaseTool
from schema import Schema, Literal

from openai_dm.character_sheet import AbilityScores


class AbilityScoreTool(BaseTool):
    def __init__(self, structure: Agent, **kwargs):
        super().__init__(**kwargs)
        self.structure = structure

    @activity(
        config={
            "description": "Updates the character sheet with an ability score distribution.",
            "schema": Schema(
                {
                    Literal(
                        "ability_scores",
                        description=f"A json of ability scores. Keys are: {list(AbilityScores.__dataclass_fields__.keys())}",  # noqa: E501
                    ): dict,
                }
            ),
        }
    )
    def update_ability_scores(self, params: dict) -> TextArtifact:
        if self.structure.conversation:
            self.structure.conversation.state = (
                self.structure.conversation.ConvStates.UPDATING_SHEET
            )

        ability_scores = params["values"]["ability_scores"].items()
        ability_scores = {k.lower(): v for k, v in ability_scores}

        base_ability_scores = AbilityScores(**ability_scores)

        self.structure.character_sheet.base_ability_scores = base_ability_scores
        self.structure.character_sheet.apply_racial_ability_bonus()
        self.structure.character_sheet.update_max_hp()

        if self.structure.conversation:
            self.structure.conversation.state = (
                self.structure.conversation.ConvStates.CHANGING_NODE
            )

        return TextArtifact("The character sheet has been updated.")
