FROM python:3.8

WORKDIR /src

COPY requirements.txt .
COPY .gitignore .

RUN apt-get update
RUN apt-get install -y vim

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN source/openai/commands.sh

CMD ["bash"]