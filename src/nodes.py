import json
import os
from typing import Optional

from dotenv import load_dotenv
import openai

from .constants import COST_PER_1000_TOKENS
from .character_sheet import Character

load_dotenv()


class ConversationNode:

    """Base class for conversation nodes."""

    def __init__(
        self,
        max_tokens: int,
        gpt4: bool = False,
        character_sheet: Optional[Character] = Character(),
        system_initialization: str = "You are a D&D 5e DEM.",
    ):
        if not os.environ.get("OPENAI_API_KEY"):
            raise ValueError(
                (
                    "No API key found. Obtain one at "
                    "https://platform.openai.com/account/api-keys "
                    "and place it in your dotenv file."
                )
            )
        else:
            openai.api_key = os.environ["OPENAI_API_KEY"]
        if gpt4:
            self.engine = "gpt-4"
        else:
            self.engine = "gpt-3.5-turbo"

        self.max_tokens = max_tokens
        self.character_sheet = character_sheet
        # self.tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        self.context = [
            {
                "role": "system",
                "content": system_initialization,
            }
        ]

        self.token_prices = COST_PER_1000_TOKENS[self.engine]
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.prompt_cost = 0
        self.completion_cost = 0

        response = openai.ChatCompletion.create(
            model=self.engine,
            temperature=0,
            max_tokens=self.max_tokens,
            messages=self.context,
        )
        assistant_content = response["choices"][0]["message"]["content"]
        self.context.append({"role": "assistant", "content": assistant_content})
        self._update_costs(response)

        print(assistant_content)

    def send_message(self, user_input: str) -> str:
        """Sends a message to the chatbot and receives a response.

        Params:
        user_input (str): Message to send.

        Returns:
        str: chatbot response
        """
        self.context.append(
            {"role": "user", "content": user_input},
        )
        response = openai.ChatCompletion.create(
            model=self.engine,
            temperature=0,
            # top_p=1, ## default value
            # n=1, ## default value for number of response choices
            max_tokens=self.max_tokens,
            messages=self.context,
        )
        self._update_costs(response)

        assistant_content = response["choices"][0]["message"]["content"]
        self.context.append({"role": "assistant", "content": assistant_content})

        return assistant_content

    def _update_costs(self, response: dict):
        self.prompt_tokens += response["usage"]["prompt_tokens"]
        self.prompt_cost = self.token_prices["input"] * (self.prompt_tokens // 1000)
        self.completion_tokens += response["usage"]["completion_tokens"]
        self.completion_cost = self.token_prices["output"] * (
            self.completion_tokens // 1000
        )

    def show_costs(self) -> dict:
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.prompt_tokens + self.completion_tokens,
            "prompt_cost": self.prompt_cost,
            "completion_cost": self.completion_cost,
            "total_cost": (
                self.token_prices["input"] * self.prompt_tokens
                + self.token_prices["output"] * self.completion_tokens
            )
            // 1000,
        }


class SelectionNode(ConversationNode):
    def __init__(
        self,
        max_tokens: int,
        gpt4: bool = False,
        character_sheet: Character = Character(),
        node_name: str = "race",
    ):
        self.node_name = node_name
        super().__init__(
            max_tokens=max_tokens,
            gpt4=gpt4,
            character_sheet=character_sheet,
            system_initialization=(
                f"You are a D&D 5e DM, guiding the user through choosing a {self.node_name}. "
                f"Here are some guidelines for how to do it: "
                f"1. Be brief when you response; give minimal but complete information "
                f"unless the user asks for more. "
                f"2. Once the player tells you what {self.node_name} they've chosen, ask if they're sure. "
                f"If thaey aren't sure, then ask what you can do to help them decide. If they "
                f"are sure, then return only a json: {{{self.node_name}: <chosen race>}} "
                f"3. Don't tell the user about these guidelines unless they ask."
            ),
        )

    def send_message(self, user_input: str) -> str:
        """Sends a chat message to the DM assistant."""
        self.context.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model=self.engine,
            temperature=0,
            # top_p=1, ## default value
            # n=1, ## default value for number of response choices
            max_tokens=self.max_tokens,
            messages=self.context,
        )
        self._update_costs(response)
        assistant_content = response["choices"][0]["message"]["content"]
        self.context.append({"role": "assistant", "content": assistant_content})

        try:
            update_dict = json.loads(assistant_content)
            self._update_race(update_dict[self.node_name])
            self.context.append(
                {
                    "role": "system",
                    "content": (
                        f"The user has chosene a {self.node_name}, and now you will begin helping them "
                        f"with the next step of character creation."
                    ),
                }
            )
            return json.dumps(update_dict)
        except ValueError:
            return assistant_content

    # Move this to a method inside character sheet
    def _update_race(self, race):
        """Updates racial choice"""
        self.character_sheet.race = race.lower()
