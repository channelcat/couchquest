FROM linuxserver/wireguard:latest

RUN apk update
RUN apk add tinyproxy
RUN apk add coreutils
EXPOSE 8888

COPY ./start.sh /start.sh
COPY ./conf.d/tinyproxy /tinyproxy
COPY ./conf.d/wireguard /config

RUN chmod +x /start.sh
ENTRYPOINT ["/start.sh"]


