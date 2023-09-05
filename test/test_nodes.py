import os

import unittest
from unittest.mock import patch
import src.nodes  # Replace with your module name

test_args = {"max_tokens": 20}


class TestNodes(unittest.TestCase):
    @patch("openai.ChatCompletion.create")
    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake-api-key"}, clear=True)
    def test_selection_node(self, mock_create):
        test_args = {
            "max_tokens": 20,
            "gpt4": False,
            "node_name": "race",
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
        node = src.nodes.SelectionNode(**test_args)
        self.assertEqual(node.context[-1]["content"], "This is a mocked response.")

        # Test when a string is input to send_message, and a string is returned
        reply = node.send_message("Say something to API.")
        self.assertEqual(reply, "This is a mocked response.")

        # Test when a string is input to send_message, and a json is returned
        mock_create.return_value["choices"][0]["message"][
            "content"
        ] = "{'race': 'human'}"
        reply = node.send_message("Say something to API.")
        self.assertEqual(reply, "{'race': 'human'}")


if __name__ == "__main__":
    unittest.main()
