from attrs import define
from schema import Schema, Literal

from griptape.artifacts import TextArtifact
from griptape.utils.decorators import activity
from griptape.structures import Agent

from openai_dm.character_sheet import SkillProficiencies
from openai_dm.tools import BaseSheetUpdateTool


@define(kw_only=True)
class BackgroundTool(BaseSheetUpdateTool):
    structure: Agent

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
    def update_sheet(self, params: dict) -> TextArtifact:
        self._before_update()
        self._execute_update(params)
        self._after_update()
        return TextArtifact(self.output_text)

    def _execute_update(self, params: dict):
        self.structure.character_sheet.background = params["values"]["background"]
        skill_proficiencies = params["values"]["skill_proficiencies"]

        for x in skill_proficiencies:
            setattr(
                self.structure.character_sheet.skill_proficiencies,
                x.lower().replace(" ", "_"),
                True,
            )
