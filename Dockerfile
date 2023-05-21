FROM python:3.11.3

RUN mkdir /src
WORKDIR /src

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install --without dev
RUN apt update
RUN apt -y upgrade
RUN apt-get -y install software-properties-common
RUN set -x \
    && add-apt-repository ppa:mc3man/trusty-media \
    && apt-get install -y --no-install-recommends \
        ffmpeg

RUN chmod a+x docker/*.sh