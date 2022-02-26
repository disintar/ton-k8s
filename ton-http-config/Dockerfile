ARG  base
FROM ${base}

WORKDIR /var/ton-work/
ADD ./simple_server.py ./

ENTRYPOINT ["python3", "simple_server.py"]
