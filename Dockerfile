FROM python:3.10-slim-bullseye

ENV PROJECT=pytel \
    BRANCH=main \
    ORG=kastaid \
    TimeZone=Asia/Jakarta \
    TERM=xterm-256color \
    DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    VIRTUAL_ENV=/venv \
    PATH=/venv/bin:/app/bin:$PATH

WORKDIR /app
COPY . .

RUN set -ex \
    && apt-get update -y && apt list --upgradeable \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        locales \
        tzdata \
        tree \
        wget \
        curl \
        git \
        python3-dev \
        python3-pip \
        python3-venv \
        python3-testresources \
        python3-libxml2 \
        gcc \
        g++ \
        neofetch \
        pkg-config \
        build-essential \
        ffmpeg \
        cairosvg \
        libavformat-dev \
        libavcodec-dev \
        libavdevice-dev \
        libavutil-dev \
        libswscale-dev \
        libswresample-dev \
        libavfilter-dev \
        libzbar0 \
        linux-libc-dev \
    && localedef --quiet -i id_ID -c -f UTF-8 -A /usr/share/locale/locale.alias id_ID.UTF-8 \
    && ln -snf /usr/share/zoneinfo/$TimeZone /etc/localtime && echo $TimeZone > /etc/timezone \
    && dpkg-reconfigure --force -f noninteractive tzdata >/dev/null 2>&1 \
    && git clone -qb $BRANCH https://github.com/$ORG/$PROJECT . \
    && python3 -m pip install -Uq pip \
    && python3 -m venv $VIRTUAL_ENV \
    && pip3 install --no-cache-dir -U -r main.txt \
    && apt-get -qqy purge --auto-remove \
        build-essential \
    && apt-get -qqy clean \
    && rm -rf -- ~/.cache /var/lib/apt/lists/* /var/cache/apt/archives/* /etc/apt/sources.list.d/* /usr/share/man/* /usr/share/doc/* /var/log/* /tmp/* /var/tmp/*

CMD ["python3", "-m", "pytel"]
