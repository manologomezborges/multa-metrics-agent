FROM python:3.7.7-slim-buster

RUN set -ex \
    && apt-get update


RUN set -ex \
    && apt-get install -y python-dbus

RUN set -ex \
    && pythonDeps=" \
        python3-dev \
        build-essential \
        pkg-config \
        libdbus-glib-1-dev \
        libgirepository1.0-dev \
        libcairo2-dev \
        gir1.2-gtk-3.0 \
        python3-gi \
    " \
    \
    && apt-get install -y --no-install-recommends $pythonDeps

RUN mkdir /device
RUN mkdir /device/credentials
RUN mkdir /device/credentials/certificates

WORKDIR /src
ADD ./ /src

ENV PYTHONPATH $PYTHONPATH:/src

RUN pip3 install -r ./etc/pip/requirements.txt
ADD etc/files/supervisor.conf    /etc/supervisor/conf.d/

# HEALTHCHECK --start-period=120s --interval=60s --retries=1 CMD curl --fail http://127.0.0.1:5000/api/ || exit 1

CMD ["bash", "/src/src/start.sh"]