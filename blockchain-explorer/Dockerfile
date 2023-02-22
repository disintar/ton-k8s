ARG  base
FROM ${base} as builder

FROM python:3.10-slim

COPY --from=builder /ton/build/blockchain-explorer/blockchain-explorer /usr/local/bin/
COPY blockchain-explorer/start.sh /


RUN apt-get update && apt-get install -y libmicrohttpd12 wget && apt-mark manual libmicrohttpd12 wget &&\
  apt-get autoremove -y && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/start.sh"]
