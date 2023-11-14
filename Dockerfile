FROM unknownxx/kastaid:PYTEL-Premium

RUN pip install --upgrade pip

ENV PROJECT=pytel \
    BRANCH=main \
    ORG=kastaid \
    VIRTUAL_ENV=/venv \
    PATH=/venv/bin:/app/bin:$PATH

RUN set -ex \
    && git clone -qb $BRANCH https://github.com/$ORG/$PROJECT . \
    && python3 -m venv $VIRTUAL_ENV \
    && pip3 install --disable-pip-version-check --no-cache-dir -U -r main.txt

CMD ["python3", "-m", "pytel"]
