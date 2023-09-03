FROM python:3.9

WORKDIR /src

RUN apt-get update
RUN apt-get install -y vim

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY .gitignore .
COPY commands.sh .

# CMD source openai/commands.sh

CMD ["bash"]