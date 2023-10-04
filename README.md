# AI Dungeon Master
This project is an automated dungeon master for D&D 5e using OpenAI. Prompt engineering and conversational agent tooling is managed with griptape, which is similar to LangChain, but allows for DAG-based workflows. Conversation with the AI is modeled as a graph. Each node of the graph is a conversational agent dedicated to a specific conversational task that has its own termination criteria and instructions how to propagate to another accessible node.

This is an early stage work in progress and is not optimized for production. In particular, the Agent tools will tend to hit the tight rate limits of OpenAI's API due tot he complexity of reasoning they implement.

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
- Within character creation, a linear conversation to select race, class, assign ability scores, select a background, and then assign skill proficiencies is implemented.
- A character sheet object persists across the entire conversation and is available to all agents, and some conversational memory is retained across agents and can be referred back to, but this complexity has greatly increased the size of API calls and introduced some rate limiting issues. Rate limit issues typically resolve on their own after enough retries.
- No API or standalone app exists at this time, but there is a demo notebook.
