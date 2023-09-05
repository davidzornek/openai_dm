import os

import unittest
from unittest.mock import patch
import src.nodes  # Replace with your module name

test_args = {"max_tokens": 20}


class TestNodes(unittest.TestCase):
    @patch("openai.ChatCompletion.create")
    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake-api-key"}, clear=True)
    def test_conversation_node(self, mock_create):
        # Configure the mock to return a specific response
        mock_create.return_value = {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1630770631,
            "model": "gpt-3.5-turbo",
            "usage": {"prompt_tokens": 56, "completion_tokens": 31, "total_tokens": 87},
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "This is a mocked response.",
                    }
                }
            ],
        }

        node = src.nodes.ConversationNode(**test_args)
        self.assertEqual(node.context[-1]["content"], "This is a mocked response.")

        costs = node.show_costs()
        self.assertEqual(
            costs,
            {
                "prompt_tokens": 56,
                "completion_tokens": 31,
                "total_tokens": 56 + 31,
                "prompt_cost": 0.0,
                "completion_cost": 0.0,
                "total_cost": 0.0,
            },
        )
        reply = node.send_message("Say something to API.")
        self.assertEqual(reply, "This is a mocked response.")

        costs = node.show_costs()
        self.assertEqual(
            costs,
            {
                "prompt_tokens": 56 * 2,
                "completion_tokens": 31 * 2,
                "total_tokens": (56 + 31) * 2,
                "prompt_cost": 0.0,
                "completion_cost": 0.0,
                "total_cost": 0.0,
            },
        )

    @patch("openai.ChatCompletion.create")
    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake-api-key"}, clear=True)
    def test_race_selection(self, mock_create):
        # Configure the mock to return a specific response
        mock_create.return_value = {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1630770631,
            "model": "gpt-3.5-turbo",
            "usage": {"prompt_tokens": 56, "completion_tokens": 31, "total_tokens": 87},
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Selected: Tiefling",
                    }
                }
            ],
        }

        node = src.nodes.RaceSelection(**test_args)
        reply = node.send_message("Yes, I'm sure about choosing tiefling.")
        self.assertEqual(node.character_sheet.race, "tiefling")

    @patch("openai.ChatCompletion.create")
    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake-api-key"}, clear=True)
    def test_class_selection(self, mock_create):
        # Configure the mock to return a specific response
        mock_create.return_value = {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1630770631,
            "model": "gpt-3.5-turbo",
            "usage": {"prompt_tokens": 56, "completion_tokens": 31, "total_tokens": 87},
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Selected: Cleric",
                    }
                }
            ],
        }

        node = src.nodes.ClassSelection(**test_args)
        reply = node.send_message("Yes, I'm sure about choosing cleric.")
        self.assertEqual(node.character_sheet.class_name, "cleric")


if __name__ == "__main__":
    unittest.main()
