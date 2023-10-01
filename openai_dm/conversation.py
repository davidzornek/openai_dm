import logging

from griptape.rules import Rule, Ruleset
from griptape.drivers import OpenAiChatPromptDriver
from griptape.memory.tool import BlobToolMemory
from griptape.memory.structure import ConversationMemory
from griptape.structures import Agent

from openai_dm.character_sheet import Character
from openai_dm.tools import CharacterSheetUpdater, CharacterSheetInspector

CONVERSATION_GRAPH = {
    "race": ["class_"],
    "class_": ["ability_scores"],
    "ability_scores": [],
}


class Conversation:
    def __init__(
        self,
        name: str = "AI Dungeon Master",
        gpt4: bool = True,
        max_tokens: int = 500,
        logger_level: int = logging.INFO,
    ):
        self.name = name
        self.main_rules = Ruleset(
            name="Character Creation Rules",
            rules=[
                Rule(
                    """You are the dungeon master of a 5e campaign, assisting the user
                     with character creation."""
                ),
                Rule(
                    """Be brief when you response; give minimal but complete information
                    unless the user asks for more."""
                ),
                Rule("""Discuss only topics related to D&D."""),
                Rule("""Whenever you see the word 'class_', treat it at 'class'."""),
            ],
        )
        self.gpt4 = gpt4
        self.max_tokens = max_tokens
        self.logger_level = logger_level
        self.agent = None
        self.test = None
        self.character_sheet = Character()
        self._start_node(node_name="race")
        self.agent.run("introduce yourself.")

    def _start_node(self, node_name: str):
        self.current_node = node_name
        if node_name[-1] == "_":
            node_name = node_name[:-1]
        additional_rules = [
            f"""You are helping the player choose a {node_name}. Once they have chosen a
            {node_name} update the character sheet with the new {node_name}""",
            '''After updating the character sheet say only "change_node"''',
        ]
        node_rules = [self.main_rules]
        node_rules.append(
            Ruleset(
                name=f"{node_name} rules", rules=[Rule(x) for x in additional_rules]
            )
        )

        self.agent = Agent(
            rulesets=node_rules,
            logger_level=self.logger_level,
            prompt_driver=OpenAiChatPromptDriver(
                model="gpt-4" if self.gpt4 else "gpt-3.5-turbo",
                max_tokens=self.max_tokens,
            ),
            memory=ConversationMemory(),
            tools=[
                CharacterSheetUpdater(
                    character_sheet=self.character_sheet,
                    output_memory={"update_race": [BlobToolMemory()]},
                ),
                CharacterSheetInspector(
                    character_sheet=self.character_sheet,
                    output_memory={"query_character_sheet": [BlobToolMemory()]},
                ),
            ],
        )
        # call to agent_run below isn't printing anything to the terminal
        print(
            f"""I'm the assistant DM, here to help with character creation.
            Let's start with choosing a {node_name}"""
        )
        return self.agent.run(
            """
            Introduce yourself to the user and tell them which part
            of character creation we're working on.
        """
        )

    def run(self, user_input: str):
        response = self.agent.run(user_input)
        if response.output.value == "change_node":
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
            return response
