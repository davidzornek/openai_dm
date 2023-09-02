import json
import os
from typing import Optional

from dotenv import load_dotenv
import openai

from .constants import COST_PER_1000_TOKENS
from .character_sheet import CharacterSheet

load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError(
        (
            "No API key found. Obtain one at https://platform.openai.com/account/api-keys "
            "and place it in your dotenv file."
        )
    )
else:
    openai.api_key = os.environ["OPENAI_API_KEY"]


class RaceSelection:
    """Chatbot for race selection node of character creation.
    
    Params:
        max_tokens (int): maximum token length of response
        gpt4 (bool): whether to use gpt-4 vs gpt-3.5-turbo
        charactersheet (CharacterSheet): Optional CharacterSheet object to use as a starting point.
    """
    def __init__(self, max_tokens: int, gpt4: bool = False, character_sheet: Optional[CharacterSheet] = CharacterSheet()):
        if gpt4:
            self.engine="gpt-4"
        else:
            self.engine = "gpt-3.5-turbo"
        
        self.max_tokens = max_tokens
        self.character_sheet = character_sheet
        # self.tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        self.context = [
            {"role": "system", "content": (
                    "You are a D&D 5e DM. Guide the player through choosing a race."
                    "Be as brief as possible with each turn in the conversation, providing "
                    "minimal, but complete information, unless the player asks for more info. "
            )}
        ]

        response = openai.ChatCompletion.create(
            model=self.engine,
            temperature=0,
            max_tokens=self.max_tokens,
            messages=self.context
        )
        
        # Add info from setup query
        self.token_prices = COST_PER_1000_TOKENS[self.engine]
        self.prompt_tokens = 0
        self.completion_tokens = 0        
        self.prompt_cost = 0
        self.completion_cost = 0

        print(response["choices"][0]["message"]["content"])


    def send_message(self, user_input: str) -> str:
        self.context.extend([
            {"role": "user", "content": user_input},
            {"role": "system", "content": (
                "If the user has chosen a race, ask whether they're sure of their choice. "
                "If they are sure, state which race was chosen in the format 'Selected: <the race that was selected>' If they aren't, say 'Race choice reset.'"
            )}
        ])
        response = openai.ChatCompletion.create(
            model=self.engine,
            temperature=0,
            max_tokens=self.max_tokens,
            messages=self.context
        )
        assistant_content = response["choices"][0]["message"]["content"]
        self.context.append({"role": "user", "content": user_input})
        
        self.prompt_tokens += response["usage"]["prompt_tokens"]
        self.prompt_cost = self.token_prices["input"] * (self.prompt_tokens // 1000)
        self.completion_tokens += response["usage"]["completion_tokens"]
        self.completion_cost = self.token_prices["output"] * (self.completion_tokens // 1000)
        
        if assistant_content.startswith("Selected: "):
            self._update_race(assistant_content.split(" ")[1])
        if assistant_content == "Race choice reset.":
            self._update_race(None)
            self.context = [
                {"role": "system", "content": (
                        "You are a D&D 5e DM. Guide the player through choosing a race."
                        "Be as brief as possible with each turn in the conversation, providing "
                        "minimal, but complete information, unless the player asks for more info. "
                )}
            ]
            response = openai.ChatCompletion.create(
                model=self.engine,
                temperature=0,
                max_tokens=self.max_tokens,
                messages=self.context
            )
            return response["choices"][0]["message"]["content"]

        return assistant_content

    def _update_race(self, race):
        """Updates racial choice"""
        self.character_sheet.race = race

    def show_costs(self) -> dict:
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.prompt_tokens + self.completion_tokens,
            "prompt_cost": self.prompt_cost,
            "completion_cost": self.completion_cost,
            "total_cost": (
                self.token_prices["input"] * self.prompt_tokens + 
                self.token_prices["output"] * self.completion_tokens
            ) // 1000
        }


# class CharacterCreator:
#     def __init__(self, max_tokens, gpt4=False):
#         if gpt4:
#             self.engine="gpt-4"
#         else:
#             self.engine = "gpt-3.5-turbo"
        
#         self.max_tokens = max_tokens
#         # self.tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        
#         response = openai.ChatCompletion.create(
#             model=self.engine,
#             temperature=0,
#             max_tokens=self.max_tokens,
#             messages=[
#                 {"role": "system", "content": (
#                     "You are a D&D 5e DM. Guide the player through choosing a race."
#                     "Be as brief as possible with each turn in the conversation, providing "
#                     "minimal, but complete information, unless the player asks for more info. "
#                     "Once they've chosen a race, Ask whether their choice is final. If "
#                     "it is final, say 'Race chosen.' Otherwise, return to the beginning "
#                     "of race selection."
#                 )},
#                 #{"role": "assistant", "content": "What race would you like to be?"},
#             ],
#         )
        
#         # Add info from setup query
#         self.token_prices = COST_PER_1000_TOKENS[self.engine]
#         self.prompt_tokens = 0
#         self.completion_tokens = 0        
#         self.prompt_cost = 0
#         self.completion_cost = 0
#         print(response["choices"][0]["message"]["content"])
#         #print(response["message"]["content"])
        
#     def send_message(self, user_input):
#         response = openai.ChatCompletion.create(
#             model=self.engine,
#             temperature=0,
#             max_tokens=self.max_tokens,
#             messages=[
#                 {"role": "user", "content": user_input}
#             ],
#         )
        
#         self.prompt_tokens += response["usage"]["prompt_tokens"]
#         self.prompt_cost = self.token_prices["input"] * (self.prompt_tokens // 1000)
#         self.completion_tokens += response["usage"]["completion_tokens"]
#         self.completion_cost = self.token_prices["output"] * (self.completion_tokens // 1000)
        
#         return response["choices"][0]["message"]["content"]
        
    # def show_costs(self):
    #     return {
    #         "prompt_tokens": self.prompt_tokens,
    #         "completion_tokens": self.completion_tokens,
    #         "total_tokens": self.prompt_tokens + self.completion_tokens,
    #         "prompt_cost": self.prompt_cost,
    #         "completion_cost": self.completion_cost,
    #         "total_cost": (
    #             self.token_prices["input"] * self.prompt_tokens + 
    #             self.token_prices["output"] * self.completion_tokens
    #         ) // 1000
    #     }