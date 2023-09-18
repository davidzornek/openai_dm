import logging

# from dotenv import load_dotenv
from griptape.utils import Chat

from openai_dm.conversation import Conversation

# load_dotenv()


def main():
    conv = Conversation(logger_level=logging.ERROR)
    Chat(conv).start()


if __name__ == "__main__":
    main()
