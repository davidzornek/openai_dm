from abc import abstractmethod
from attr import define, field

from griptape.structures import Agent
from griptape.artifacts import TextArtifact
from griptape.utils.decorators import activity
from griptape.tools import BaseTool
from schema import Schema, Literal


@define
class BaseSheetUpdateTool(BaseTool):
    structure: Agent
    output_text: str = field(default="The character sheet has been updated.")

    @activity(
        config={
            "description": "This is a default description",
            "schema": Schema(
                {
                    Literal(
                        "placholder arg",
                        description="Just a placeholder for the base class. Will be overwritten in subclasses.",  # noqa: E501
                    ): str,
                }
            ),
        }
    )
    @abstractmethod
    # The method itself should stay the same when defined in subclasses.
    # This is made into an abstractmethod mostly to force writing
    # the activity decorator when it's subclassed.
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
