from typing import Optional

from .character_sheet import Character
from .nodes import RaceSelection, ClassSelection

CONVERSATION_GRAPH = {
    "race": ["class"],
    "class": [],
}

NODE_MAP = {"race": RaceSelection, "class": ClassSelection}


class Conversation:
    def __init__(
        self,
        max_tokens: int,
        gpt4: bool = False,
        character_sheet: Optional[Character] = Character(),
        start_node: str = "race",
    ):
        self.max_tokens = max_tokens
        self.gpt4 = gpt4
        self.current_node_name = start_node
        self.current_node = NODE_MAP[start_node](max_tokens, gpt4, character_sheet)
        self.history = []
        self.character_sheet = self.current_node.character_sheet
        self.costs = None
        self._update_costs()

    def send_message(self, user_input):
        """Sends a message to the AI dm"""
        reply = self.current_node.send_message(user_input)
        if reply.startswith("Selected: "):
            self.history.append(self.current_node)
            self._update_costs()
            self.character_sheet = self.current_node.character_sheet
            if CONVERSATION_GRAPH[self.current_node_name]:
                self.current_node_name = CONVERSATION_GRAPH[self.current_node_name][0]
                print(self.current_node_name)
                self.current_node = NODE_MAP[self.current_node_name](
                    self.max_tokens, self.gpt4, self.character_sheet
                )
            else:
                print("all done!")
        else:
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
