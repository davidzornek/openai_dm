FROM python:3.11

WORKDIR /openai_dm

RUN apt-get update
RUN apt-get install -y vim

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY .gitignore .
COPY on_start.sh .
COPY secrets.sh .
RUN chmod +x on_start.sh
RUN chmod +x secrets.sh

# ENTRYPOINT ["/bin/bash", "./on_start.sh"]
CMD [ "/bin/bash" ]