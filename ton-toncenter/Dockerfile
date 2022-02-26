ARG  base
FROM ${base}

RUN git clone https://github.com/toncenter/ton-http-api.git

WORKDIR ton-http-api

RUN rm -f ./pyTON/distlib/linux/libtonlibjson.so
RUN mv /ton/build/tonlib/libtonlibjson.so.0.5 ./pyTON/distlib/linux/libtonlibjson.so

# latest commit in master
RUN git checkout 5d1717c

# fix /api/v2
RUN sed -i 's/\/api\/v2/\//g' ./pyTON/main.py

RUN python3 -m pip install -r ./infrastructure/requirements/main.txt

ADD ./entrypoint.sh ./

ENTRYPOINT './entrypoint.sh'