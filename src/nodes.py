import os
from typing import Optional

from dotenv import load_dotenv
import openai

from .constants import COST_PER_1000_TOKENS
from .character_sheet import Character

load_dotenv()
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


class ConversationNode:
    """Base class for conversation nodes."""

    def __init__(
        self,
        max_tokens: int,
        gpt4: bool = False,
        character_sheet: Optional[Character] = Character(),
        system_initialization: str = "You are a D&D 5e DEM.",
    ):
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
        self._update_costs(response)

        print(response["choices"][0]["message"]["content"])

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


class RaceSelection(ConversationNode):
    """Chatbot for race selection node of character creation.

    Params:
        max_tokens (int): maximum token length of response
        gpt4 (bool): whether to use gpt-4 vs gpt-3.5-turbo
        character_sheet (Character): Optional Character object to use as a starting point.
    """

    def __init__(
        self,
        max_tokens: int,
        gpt4: bool = False,
        character_sheet: Optional[Character] = None,
    ):
        super().__init__(
            max_tokens=max_tokens,
            gpt4=gpt4,
            character_sheet=character_sheet,
            system_initialization=(
                "You are a D&D 5e DM. Guide the player through choosing a race."
                "Be as brief as possible with each turn in the conversation, "
                "providing minimal, but complete information, unless the player "
                "asks for more info. "
            ),
        )

    def send_message(self, user_input):
        self.context.extend(
            [
                {"role": "user", "content": user_input},
                {
                    "role": "system",
                    "content": (
                        "If the user has chosen a race, ask whether they're sure of "
                        "their choice. If they are sure reply in the format 'Selected: "
                        " <race the player chose>'. If they aren't, say 'reset'."
                    ),
                },
            ]
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

        if assistant_content.startswith("Selected: "):
            self._update_race(assistant_content.split(" ")[1])

        if assistant_content == "reset":
            self._update_race(None)
            self.context = [
                {
                    "role": "system",
                    "content": (
                        "You are a D&D 5e DM. Guide the player through choosing a race."
                        "Be as brief as possible with each turn in the conversation, providing "
                        "minimal, but complete information, unless the player asks for more info. "
                    ),
                }
            ]
            response = openai.ChatCompletion.create(
                model=self.engine,
                temperature=0,
                max_tokens=self.max_tokens,
                messages=self.context,
            )
            return response["choices"][0]["message"]["content"]

        return assistant_content

    def _update_race(self, race):
        """Updates racial choice"""
        self.character_sheet.race = race


class ClassSelection(ConversationNode):
    """Chatbot for class selection node of character creation.

    Params:
        max_tokens (int): maximum token length of response
        gpt4 (bool): whether to use gpt-4 vs gpt-3.5-turbo
        character_sheet (Character): Optional Character object to use as a starting point.
    """

    def __init__(
        self,
        max_tokens: int,
        gpt4: bool = False,
        character_sheet: Optional[Character] = None,
    ):
        super().__init__(
            max_tokens=max_tokens,
            gpt4=gpt4,
            system_initialization=(
                "You are a D&D 5e DM. Guide the player through choosing a class."
                "Be as brief as possible, providing minimal, but complete information, unless the user "
                "asks for more info. "
            ),
        )

    def send_message(self, user_input):
        self.context.extend(
            [
                {"role": "user", "content": user_input},
                {
                    "role": "system",
                    "content": (
                        "If the user has chosen a class, ask whether they're sure of "
                        "their choice. If they are sure reply in the format 'Selected: "
                        " <class the player chose>'. If they aren't, say 'reset'."
                    ),
                },
            ]
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

        if assistant_content.startswith("Selected: "):
            self._update_class(assistant_content.split(" ")[1])

        if assistant_content == "reset":
            self._update_class(None)
            self.context = [
                {
                    "role": "system",
                    "content": (
                        "You are a D&D 5e DM. Guide the player through choosing a class."
                        "Be as brief as possible with each turn in the conversation, providing "
                        "minimal, but complete information, unless the player asks for more info. "
                    ),
                }
            ]
            response = openai.ChatCompletion.create(
                model=self.engine,
                temperature=0,
                max_tokens=self.max_tokens,
                messages=self.context,
            )
            return response["choices"][0]["message"]["content"]

        return assistant_content

    def _update_class(self, class_name):
        """Updates racial choice"""
        self.character_sheet.class_name = class_name
