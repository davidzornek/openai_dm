from attrs import define

from griptape.structures import Agent
from schema import Schema, Literal

from griptape.artifacts import TextArtifact
from griptape.utils.decorators import activity

from openai_dm.character_sheet import AbilityScores
from openai_dm.tools import BaseSheetUpdateTool


@define(kw_only=True)
class AbilityScoreTool(BaseSheetUpdateTool):
    structure: Agent

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
    def update_sheet(self, params: dict) -> TextArtifact:
        self._before_update()
        self._execute_update(params)
        self._after_update()
        return TextArtifact(self.output_text)

    def _execute_update(self, params: dict):
        ability_scores = params["values"]["ability_scores"].items()
        ability_scores = {k.lower(): v for k, v in ability_scores}

        base_ability_scores = AbilityScores(**ability_scores)

        self.structure.character_sheet.base_ability_scores = base_ability_scores
        self.structure.character_sheet.apply_racial_ability_bonus()
        self.structure.character_sheet.update_max_hp()
