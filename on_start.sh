#!/bin/bash

source secrets.sh;

function build_image {
    docker build -t dm .;
}
function run_image { 
    docker rm dm;
    docker run -v ~/Documents/nlp/openai_dm/:/openai_dm/ -it -p 8888:8888 --name dm dm bash;
}
function enter_image {
    docker exec -it dm bash;
}
function jupyter_up {
    jupyter notebook --allow-root --no-browser --ip=0.0.0.0 --port=8888;
}

jupyter notebook --allow-root --no-browser --ip=0.0.0.0 --port=8888