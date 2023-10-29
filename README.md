# AI Dungeon Master
This project is an automated dungeon master for D&D 5e using OpenAI. Prompt engineering and conversational agent tooling is managed with griptape, which is similar to LangChain, but allows for DAG-based workflows. Conversation with the AI is modeled as a graph. Each node of the graph is a conversational agent dedicated to a specific conversational task that has its own termination criteria and instructions how to propagate to another accessible node.

### How to run the demo notebook
Set up your API Key:
- Visit https://platform.openai.com/account/api-keys to get an API Key.
- `cp .env.example .env`
- Edit `.env` to set `OPENAI_API_KEY` as your api key.

To run the example notebook:
- `docker build -t dm .`
- `docker run -v <path to local repo>:/src/ -p 8888:8888 -it --name dm dm bash`
- `jupyter notebook --allow-root --no-browser --ip=0.0.0.0 --port=8888`
- Copy paste the url from jupyter into your web browser, and open `Example.ipynb`.

### Known limitations at the current state of development
- Currently, only character creation is supported.
- Within character creation, a linear conversation to select race, class, assign ability scores, select a background, and then assign skill proficiencies is implemented. In the future, the user will be able to set their own path through character creation and will be able to return to prior nodes if needed.
- A character sheet object persists across the entire conversation and is available to all agents, and some conversational memory is retained across agents and can be referred back to.
- As conversation memory accumulates and prompt size increases, some instructions in the base react prompt are getting "lost" at laster stages of the conversation, causing a failure to call character sheet updating tools, even though the chatbot will tell
the user that the character sheet has been updated. Telling the chatbot that it forgot to update the character sheet will generally trigger the tool to be called.
- No API or standalone app exists at this time, but there is a demo notebook.
