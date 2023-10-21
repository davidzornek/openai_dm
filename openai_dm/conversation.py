from attr import define, field, Factory
import logging

# from griptape.rules import Rule, Ruleset
# from griptape.drivers import OpenAiChatPromptDriver
from griptape.memory.structure import ConversationMemory

from openai_dm.dm_kit import DMAgent
from openai_dm.character_sheet import Character
from openai_dm.tools import CharacterSheetUpdater
from openai_dm.constants import NODE_TOOLS

CONVERSATION_GRAPH = {
    "race": ["class_"],
    "class_": ["ability_scores"],
    "ability_scores": ["background"],
    "background": ["skill_proficiencies"],
    "skill_proficiencies": [],
}


@define
class CharacterCreationConversation:
    name: str = field(default="AI Dungeon Master")
    gpt4: bool = field(default=True)
    max_tokens: int = field(default=500)
    logger_level: int = field(default=logging.INFO)
    starting_node: str = field(default="race")
    character_sheet: Character = field(default=Factory(lambda: Character()))
    agent: DMAgent = field(default=None)
    memory: ConversationMemory = field(default=Factory(lambda: ConversationMemory()))

    def __attrs_post_init__(self):
        self.agent = DMAgent(
            character_sheet=self.character_sheet,
            tools=NODE_TOOLS[self.starting_node],
            node=self.starting_node,
            memory=self.memory,
            logger_level=self.logger_level,
        )
        response = self.agent.run(
            "Introduce yourself and introduce the player the character creation."
        )
        print(response.output.value)

    #     self._start_node(node_name=self.starting_node)
    #     if node_name[-1] == "_":
    #         node_name = node_name[:-1]

    # def _start_node(self, node_name: str):
    #     self.current_node = node_name
    #     self.agent

    #     node_rules = [self.main_rules]
    #     node_rules.append(
    #         Ruleset(
    #             name="node_initalization_rules",
    #             rules=[Rule(x) for x in node_initialization_rules],
    #         )
    #     )
    #     node_rules.append(
    #         Ruleset(
    #             name=f"{node_name} rules",
    #             rules=[Rule(x) for x in NODE_RULES[self.current_node]],
    #         )
    #     )

    #     self.agent = DMAgent(
    #         character_sheet=self.character_sheet,
    #         rulesets=node_rules,
    #         logger_level=self.logger_level,
    #         prompt_driver=OpenAiChatPromptDriver(
    #             model="gpt-4" if self.gpt4 else "gpt-3.5-turbo-0613",
    #             max_tokens=self.max_tokens,
    #         ),
    #         memory=self.memory,
    #     )
    #     response = self.agent.run(
    #         f"""
    #         If first_run==True, then introduce yourself, tell them
    #         you're here to help them with character creation, as well as what you're
    #         going to start with. Regarldess of whether this is the first run,
    #         give them any basic information they might need for selecting a {node_name}
    #         first_run=={self.first_run}
    #         """
    #     )
    #     print(response.output.value)
    #     return response

    def run(self, user_input: str):
        response = self.agent.run(user_input)
        if response.output.value == "change_node":
            self.first_run = False
            character_sheet_updater = [
                x for x in self.agent.tools if isinstance(x, CharacterSheetUpdater)
            ][0]
            self.character_sheet = character_sheet_updater.character_sheet

            if CONVERSATION_GRAPH[self.current_node] == []:
                print("all done!")
                return "All done!"
            else:
                next_node = CONVERSATION_GRAPH[self.current_node][0]
                self.agent.run(
                    f"""You've just helped the user select a {self.current_node},
                    and next you will help them select a {next_node}. Let the
                    user know that their choice has been logged to their character
                    sheet and tell them what's next.
                    """
                )
                self.current_node = next_node

            return self._start_node(self.current_node)
        else:
            print(response.output.value)
            return response
