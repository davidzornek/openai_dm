function build_image { docker build -t openai .; }
function run_image { 
    docker run -v ~/Documents/nlp/openai/:/src/openai/ -it -p 8888 --name openai_dev openai bash 
}
function enter_image {
    docker exec -it openai_dev
}
function jupyter_up {
    jupyter notebook --allow-root --no-browser --ip=0.0.0.0 --port=8888
}