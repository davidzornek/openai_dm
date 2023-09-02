import json
import os

from dotenv import load_dotenv
import openai

from constants import COST_PER_1000_TOKENS

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


class Conversation:
    def __init__(self, engine, max_tokens):
        self.engine = engine
        self.max_tokens = max_tokens
        # self.tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

        self.token_prices = COST_PER_1000_TOKENS[self.engine]
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.prompt_cost = 0
        self.completion_cost = 0

    def send_message(self, user_input):
        response = openai.ChatCompletion.create(
            model=self.engine,
            temperature=0,
            max_tokens=self.max_tokens,
            messages=[
                {"role": "system", "content": "You are a D&D 5e DM."},
                {"role": "user", "content": "What class should I be?"},
                {"role": "assistant", "content": "Whatever you want!"},
                {"role": "user", "content": "What are fighters like?"},
            ],
        )

        self.prompt_tokens += response["usage"]["prompt_tokens"]
        self.prompt_cost = self.token_prices["input"] * (self.prompt_tokens // 1000)
        self.completion_tokens += response["usage"]["completion_tokens"]
        self.completion_cost = self.token_prices["output"] * (
            self.completion_tokens // 1000
        )

        return response

    def show_costs(self):
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
