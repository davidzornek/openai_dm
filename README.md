To run the example notebook:
- `docker build -t dm .`
- `docker run -v <path to local repo>:/src/openai_dm/ -p 8888:8888 -it --name dm_dev dm bash`
- `jupyter notebook --allow-root --ip=0.0.0.0 --port=8888`