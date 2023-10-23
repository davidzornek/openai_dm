from abc import abstractmethod
from attr import define, field

from griptape.structures import Agent
from griptape.artifacts import TextArtifact
from griptape.utils.decorators import activity
from griptape.tools import BaseTool
from schema import Schema


@define
class BaseSheetUpdateTool(BaseTool):
    structure: Agent
    description: str
    schema: Schema
    output_text: str = field(default="The character sheet has been updated.")

    def __attrs_post_init__(self):
        self.update_sheet = activity(
            config={"description": self.description, "schema": self.schema}
        )(self.update_sheet)

    def update_sheet(self, params: dict) -> TextArtifact:
        self._before_update()
        self._execute_update(params)
        self._after_update()
        return TextArtifact(self.output_text)

    def _before_update(self):
        if self.structure.conversation:
            self.structure.conversation.state = (
                self.structure.conversation.ConvStates.UPDATING_SHEET
            )

    def _after_update(self):
        if self.structure.conversation:
            self.structure.conversation.state = (
                self.structure.conversation.ConvStates.CHANGING_NODE
            )

    @abstractmethod
    def _execute_update(self, params: dict):
        """Abstract method for the sheet updating procedure that will be called
        while the converstation status is set to UPDATING_SHEET.

        Here's an example of updating abiliy scores:

        ability_scores = params["values"]["ability_scores"].items()
        ability_scores = {k.lower(): v for k, v in ability_scores}

        base_ability_scores = AbilityScores(**ability_scores)

        self.structure.character_sheet.racn = base_ability_scores
        self.structure.character_sheet.apply_racial_ability_bonus()
        self.structure.character_sheet.update_max_hp()"""
        pass
