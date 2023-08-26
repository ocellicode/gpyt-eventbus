FROM python:3.11

ARG VERSION=0.0.6
ARG LABEL=${VERSION}

RUN python3 -m pip install --extra-index-url https://test.pypi.org/simple/ gpyt_eventbus==${VERSION}
COPY ./alembic.ini ./alembic.ini
COPY ./alembic ./alembic
COPY ./entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

CMD ["./entrypoint.sh"]
