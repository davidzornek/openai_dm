FROM python:3.9

WORKDIR /openai_dm

RUN apt-get update
RUN apt-get install -y vim

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY .gitignore .
COPY commands.sh .

CMD ["jupyter", "--allow-root", "--no-browser", "--ip=0.0.0.0", "--port=8888"]