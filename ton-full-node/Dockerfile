FROM registry.head-labs.com/ton/ton-base:v0

ENV PUBLIC_IP 0.0.0.0
ENV CONFIG https://test.ton.org/ton-global.config.json
ENV CONSOLE_PORT 46731
ENV LITESERVER true
ENV LITE_PORT true

ENTRYPOINT ["/var/ton-work/db/init.sh"]
