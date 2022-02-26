wget $CONFIG -O liteserver_config.json

jupyter notebook --ip=0.0.0.0 --port=${JUPYTER_PORT} --allow-root --notebook-dir=/opt/examples &

gunicorn pyTON.main:app -k uvicorn.workers.UvicornWorker -w ${TON_API_WEBSERVERS_WORKERS} --bind 0.0.0.0:${PORT}