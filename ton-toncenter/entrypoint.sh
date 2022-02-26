wget $CONFIG -O liteserver_config.json

gunicorn pyTON.main:app -k uvicorn.workers.UvicornWorker -w ${TON_API_WEBSERVERS_WORKERS} --bind 0.0.0.0:${PORT}