from abc import ABC
from attr import define, field, Factory
from enum import Enum
import logging

from griptape.memory.structure import ConversationMemory

from openai_dm.dm_kit import DMAgent
from openai_dm.character_sheet import Character
from openai_dm.constants import NODE_TOOLS

CONVERSATION_GRAPH = {
    "race": ["class_"],
    "class_": ["ability_scores"],
    "ability_scores": ["background"],
    "background": ["skill_proficiencies"],
    "skill_proficiencies": [],
}


@define
class CharacterCreationConversation(ABC):
    name: str = field(default="AI Dungeon Master")
    gpt4: bool = field(default=True)
    max_tokens: int = field(default=500)
    logger_level: int = field(default=logging.INFO)
    current_node: str = field(default="race")
    character_sheet: Character = field(default=Factory(lambda: Character()))
    agent: DMAgent = field(default=None)
    memory: ConversationMemory = field(default=Factory(lambda: ConversationMemory()))
    state: str = field(default=None)

    def __attrs_post_init__(self):
        self.state = CharacterCreationConversation.ConvStates.CONVERSING
        self.agent = DMAgent(
            character_sheet=self.character_sheet,
            tools=NODE_TOOLS[self.current_node],
            node=self.current_node,
            memory=self.memory,
            logger_level=self.logger_level,
            conversation=self,
        )
        response = self.agent.run(
            "Introduce yourself and introduce the player the character creation."
        )
        print(response.output.value)

    class ConvStates(Enum):
        CONVERSING = 1
        UPDATING_SHEET = 2
        CHANGING_NODE = 3

    def run(self, user_input: str):
        response = self.agent.run(user_input)
        if self.state == self.ConvStates.CHANGING_NODE:
            if CONVERSATION_GRAPH[self.current_node] == []:
                print("all done!")
                return "All done!"
            else:
                next_node = CONVERSATION_GRAPH[self.current_node][0]
                last_node = self.current_node
                self.current_node = next_node
                self.state = CharacterCreationConversation.ConvStates.CONVERSING
                self.agent = DMAgent(
                    character_sheet=self.character_sheet,
                    tools=NODE_TOOLS[self.current_node],
                    node=self.current_node,
                    memory=self.memory,
                    logger_level=self.logger_level,
                    conversation=self,
                )
                response = self.agent.run(
                    f"""You've just helped the user select a {last_node},
                    and next you will help them select a {self.current_node}. Let the
                    user know that their choice has been logged to their character
                    sheet and tell them what's next.
                    """
                )

        print(response.output.value)
        return response
