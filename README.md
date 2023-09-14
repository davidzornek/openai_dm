# AI Dungeon Master
This project is an automated dungeon master for D&D 5e using OpenAI. Prompt engineering is managed with griptape.
Currently, only character creation is supported.

Set up your API Key:
- Visit https://platform.openai.com/account/api-keys to get an API Key.
- `cp .env.example .emv`
- Edit `.env` to set `OPENAI_API_KEY` as your api key.

To run the example notebook:
- `docker build -t dm .`
- `docker run -v <path to local repo>:/openai_dm/ -p 8888:8888 -it --name dm_dev dm bash`
- Copy paste the url from jupyter into your web browser, and open `Example.ipynb`.
