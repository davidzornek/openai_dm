import os

import unittest
from unittest.mock import patch
from openai_dm import conversation


class TestConversation(unittest.TestCase):
    @patch("openai.ChatCompletion.create")
    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake-api-key"}, clear=True)
    def test_conversation(self, mock_create):
        test_args = {
            "max_tokens": 20,
            "gpt4": False,
            "start_node_name": "race",
        }

        mock_create.return_value = {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1630770631,
            "model": "gpt-3.5-turbo",
            "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20},
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "This is a mocked response.",
                    }
                }
            ],
        }

        # Test Instantiation
        conv = conversation.Conversation(**test_args)
        self.assertEqual(
            conv.current_node.context[-1]["content"], "This is a mocked response."
        )

        # Test when a string is input to send_message, and a string is returned
        reply = conv.send_message("Say something to API.")
        self.assertEqual(reply, "This is a mocked response.")

        # Test when a string is input to send_message, and a json is returned, triggering
        # conversation to advance to the next node
        mock_create.return_value["choices"][0]["message"][
            "content"
        ] = '{"race": "human"}'
        reply = conv.send_message("Say something to API.")
        self.assertEqual(reply, '{"race": "human"}')
        self.assertEqual(conv.character_sheet.race, "human")
        self.assertEqual(conv.current_node_name, "class_name")


if __name__ == "__main__":
    unittest.main()
