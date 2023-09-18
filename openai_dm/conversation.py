import json
import logging

from griptape.rules import Rule, Ruleset
from griptape.drivers import OpenAiChatPromptDriver
from griptape.memory.structure import ConversationMemory
from griptape.structures import Agent

from .character_sheet import Character

CONVERSATION_GRAPH = {
    "race": ["class_"],
    "class_": ["ability_scores"],
    "ability_Scores": [],
}


class Conversation:
    def __init__(
        self,
        name: str = "AI Dungeon Master",
        gpt4: bool = True,
        max_tokens: int = 100,
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
        additional_rules = [
            f"""You are helping the player choose a {node_name}. Once they have chosen a
            {node_name}, return only a json: {{{{ {node_name}: chosen {node_name} }}}}"""
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
        )
        return self.agent.run(
            """
            Introduce yourself to the user and tell them which part
            of character creation we're working on.
        """
        )

    def run(self, user_input: str):
        output_task = self.agent.run(user_input)
        try:
            update_json = json.loads(output_task.output.value)
            if "class" in update_json.keys():
                update_json["class_"] = update_json.pop("class")
                self.current_node = "class_"
            self.character_sheet.update(update_json)

            print(self.current_node)
            next_node = CONVERSATION_GRAPH[self.current_node][0]
            print(next_node)
            if next_node == []:
                print("all done!")
                return "All done!"
            else:
                self.agent.run(
                    f"""You've just helped the user select a {self.current_node},
                    and next you will help them select a {next_node}. Let the
                    user know that their choice has been logged to their character
                    sheet and tell them what's next.
                    """
                )
                self.current_node = next_node

            if self.current_node == "class_":
                return self._start_node(self.current_node[:-1])
            else:
                return self._start_node(self.current_node)
        except ValueError:
            return output_task
