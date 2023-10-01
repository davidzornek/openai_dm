# AI Dungeon Master
This project is an automated dungeon master for D&D 5e using OpenAI. Prompt engineering and conversational agent tooling is managed with griptape, which is similar to LangChain, but allows for DAG-based workflows.

### How to run the demo notebook
Set up your API Key:
- Visit https://platform.openai.com/account/api-keys to get an API Key.
- `cp .env.example .env`
- Edit `.env` to set `OPENAI_API_KEY` as your api key.

To run the example notebook:
- `docker build -t dm .`
- `docker run -v <path to local repo>:/openai_dm/ -p 8888:8888 -it --name dm dm bash`
- `jupyter notebook --allow-root --no-browser --ip=0.0.0.0 --port=8888`
- Copy paste the url from jupyter into your web browser, and open `Example.ipynb`.

### Known limitations at the current state of development
- Currently, only character creation is supported.
- Within character creation, a linear conversation to select race, class, and assign ability scores is implemented.
- The total conversation is modeled as a graph, looking forward to more non-linear conversational patterns. Each node of the graph is a conversational agent dedicated to that aspect of character creation.
- A character sheet object persists across the entire conversation and is available to all agents, but no other memory persists across agents, and the AI will behave as though it's beginning an entirely new conversation.
- No API or standalone app exists at this time, but there is a demo notebook.
