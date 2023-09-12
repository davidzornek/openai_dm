import json

from griptape.rules import Rule, Ruleset
from griptape.drivers import OpenAiChatPromptDriver
from griptape.memory.structure import ConversationMemory
from griptape.structures import Agent

from .character_sheet import Character

CONVERSATION_GRAPH = {
    "race": ["class_"],
    "class_": [],
}


class Conversation:
    def __init__(
        self, name: str = "AI Dungeon Master", gpt4: bool = True, max_tokens: int = 100
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
            ],
        )
        self.gpt4 = gpt4
        self.max_tokens = max_tokens
        self.agent = None
        self.test = None
        self.character_sheet = None

    def _start_node(self, node_name="race"):
        self.current_node = node_name
        self.character_sheet = Character()
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
            prompt_driver=OpenAiChatPromptDriver(
                model="gpt-4" if self.gpt4 else "gpt-3.5-turbo",
                max_tokens=self.max_tokens,
            ),
            memory=ConversationMemory(),
        )

    def run(self, user_input: str):
        output_task = self.agent.run(user_input)
        try:
            update_json = json.loads(output_task.output.value)
            if "class" in update_json.keys():
                update_json["class_"] = update_json.pop("class")
            self.character_sheet.update(update_json)

            next_node = CONVERSATION_GRAPH[self.current_node]
            if next_node == []:
                print("all done!")
                return "All done!"
            else:
                self.current_node = next_node

            if self.current_node == "class_":
                self._start_node(self.current_node[:-1])
            else:
                self._start_node(self.current_node)
        except ValueError:
            pass
