import logging

# from dotenv import load_dotenv
from griptape.structures import Agent
from griptape.utils import Chat  #   <-- Added Chat

from openai_dm.conversation import Conversation

# load_dotenv()


def main():
    conv = Conversation(logger_level=logging.ERROR)
    Chat(Conversation(logger_level=logging.ERROR)).start()


if __name__ == "__main__":
    main()
