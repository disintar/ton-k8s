ARG  CODE_VERSION=latest
FROM registry.head-labs.com/ton/ton-base:${CODE_VERSION}

# ENV PUBLIC_IP 94.130.163.226
# ENV CONFIG https://test.ton.org/ton-global.config.json
# ENV CONSOLE_PORT 46731
# ENV LITESERVER true
# ENV LITE_PORT 46732

ENTRYPOINT ["python3", "/var/ton-work/db/scripts/init_ton.py"]
