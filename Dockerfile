FROM unknownxx/kastaid:PYTEL-Premium

ENV VIRTUAL_ENV=/venv

COPY . .

RUN set -ex \
    && python3 -m venv $VIRTUAL_ENV \
    && python3 -m pip install -Uq pip \
    && pip3 install --no-cache-dir -U -r main.txt \
    && apt-get -qqy purge --auto-remove \
        build-essential \
    && apt-get -qqy clean \
    && rm -rf -- ~/.cache /var/lib/apt/lists/* \
       /var/cache/apt/archives/* \
       /etc/apt/sources.list.d/* \
       /usr/share/man/* \
       /usr/share/doc/* \
       /var/log/* /tmp/* /var/tmp/*

CMD ["python3", "-m", "pytel"]
