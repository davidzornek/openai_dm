import os

import unittest
from unittest.mock import patch
from openai.openai_object import OpenAIObject

from openai_dm import conversation


def create_openai_object(payload: dict) -> OpenAIObject:
    obj = OpenAIObject()
    message = OpenAIObject()
    content = OpenAIObject()
    content.content = payload.get("content")
    content.role = payload.get("role")
    message.message = content
    obj.choices = [message]
    return obj


class TestConversation(unittest.TestCase):
    @patch("openai.ChatCompletion.create")
    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake-api-key"}, clear=True)
    @unittest.skip(
        """Libraries in flux, so we don't have a stable output structure.
    """
    )
    def test_conversation(self, mock_create):
        test_args = {
            "max_tokens": 20,
            "gpt4": False,
        }

        mock_create.return_value = create_openai_object(
            {
                "role": "assistant",
                "content": "This is a mocked response.",
            }
        )

        # Test Instantiation
        conv = conversation.Conversation(**test_args)
        # Test when a string is input to send_message, and a string is returned
        reply = conv.run("Say something to API.")
        self.assertEqual(reply.output.value, "This is a mocked response.")


if __name__ == "__main__":
    unittest.main()
