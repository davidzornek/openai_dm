from attr import field, Factory
from typing import Callable

from griptape.memory.tool import BlobToolMemory
from griptape.structures import Agent
from griptape.tasks import ToolkitTask, ActionSubtask
from griptape.utils import J2

from openai_dm.tools import CharacterSheetInspector, CharacterSheetUpdater


class DMAgent(Agent):
    def __init__(self, character_sheet):
        super().__init__()
        self.character_sheet = character_sheet
        self.tools = [
            CharacterSheetUpdater(
                character_sheet=self.character_sheet,
            ),
            CharacterSheetInspector(
                character_sheet=self.character_sheet,
                output_memory={"query_character_sheet": [BlobToolMemory()]},
            ),
        ]
        self.add_task(DMToolkitTask(self.input_template, tools=self.tools))


class DMToolkitTask(ToolkitTask):
    def __attrs_post_init__(self):
        self.generate_assistant_subtask_template: Callable[
            [ActionSubtask], str
        ] = field(
            default=Factory(
                lambda self: self.default_assistant_subtask_template_generator,
                takes_self=True,
            ),
            kw_only=True,
        )

    def assistant_subtask_template_generator(self, subtask: ActionSubtask) -> str:
        return J2("openai_dm/templates/assistant_subtask.j2").render(subtask=subtask)
