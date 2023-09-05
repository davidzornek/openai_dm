import json
from typing import Optional

from .character_sheet import Character
from .nodes import SelectionNode

CONVERSATION_GRAPH = {
    "race": ["class"],
    "class": [],
}

# NODE_MAP = {"race": RaceSelection, "class": ClassSelection}


class Conversation:
    def __init__(
        self,
        max_tokens: int,
        gpt4: bool = False,
        character_sheet: Optional[Character] = Character(),
        start_node_name: str = "race",
    ):
        self.max_tokens = max_tokens
        self.gpt4 = gpt4
        self.character_sheet = character_sheet
        self.current_node_name = start_node_name

        self.current_node = SelectionNode(
            self.max_tokens, self.gpt4, self.character_sheet, self.current_node_name
        )
        self.history = []
        self.costs = None
        self._update_costs()

    def send_message(self, user_input):
        """Sends a message to the AI dm"""
        reply = self.current_node.send_message(user_input)
        try:
            reply = json.loads(reply)

            self.history.append(self.current_node)
            self._update_costs()
            self.character_sheet = self.current_node.character_sheet
            if CONVERSATION_GRAPH[self.current_node_name]:
                self.current_node_name = CONVERSATION_GRAPH[self.current_node_name][0]
                self.current_node = SelectionNode(
                    self.max_tokens,
                    self.gpt4,
                    self.character_sheet,
                    self.current_node_name,
                )
            else:
                print("all done!")
        except ValueError:
            return reply

    def _update_costs(self):
        if not self.costs:
            self.costs = {
                "prompt_tokens": self.current_node.prompt_tokens,
                "completion_tokens": self.current_node.completion_tokens,
                "prompt-cost": self.current_node.prompt_cost,
                "completion_cost": self.current_node.completion_cost,
            }
        else:
            self.costs["prompt_tokens"] += self.current_node.prompt_tokens
            self.costs["completion_tokens"] += self.current_node.completion_tokens
            self.costs["prompt-cost"] += self.current_node.prompt_cost
            self.costs["completion_cost"] += self.current_node.completion_cost
