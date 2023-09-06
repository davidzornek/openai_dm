function build_image { docker build -t dm .; }
function run_image { 
    docker run -v ~/Documents/nlp/openai_dm/:/openai_dm/ -it -p 8888:8888 --name dm dm bash 
}
function enter_image {
    docker exec -it openai_dev bash;
}
function jupyter_up {
    jupyter notebook --allow-root --no-browser --ip=0.0.0.0 --port=8888
}