ARG  base
FROM ${base}

RUN git clone https://github.com/toncenter/ton-http-api.git

WORKDIR ton-http-api

# latest commit is master
RUN git checkout 5d1717c

# fix /api/v2
RUN sed -i 's/\/api\/v2/\//g' ./pyTON/main.py

RUN python3 -m pip install -r ./infrastructure/requirements/main.txt

ADD ./entrypoint.sh ./

ENTRYPOINT './entrypoint.sh'