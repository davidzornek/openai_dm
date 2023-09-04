import unittest
from unittest.mock import patch
import src.nodes  # Replace with your module name

test_args = {"max_tokens": 20}


class TestNodes(unittest.TestCase):
    @patch("openai.ChatCompletion.create")
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

        # Call your function that uses openai.ChatCompletion.create
        node = src.nodes.ConversationNode(**test_args)
        print(node)
        # Assert that the result matches what you expect
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


if __name__ == "__main__":
    unittest.main()
