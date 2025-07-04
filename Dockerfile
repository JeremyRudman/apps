FROM node:22-bookworm AS build-lazer

WORKDIR /code/lazer_app/projectLazer/
COPY ./ /code/

RUN --mount=type=cache,target=/root/.npm,sharing=locked \
    npm install

RUN npx ionic build --prod


FROM python:3.13-bullseye

RUN set -eux; \
    rm -f /etc/apt/apt.conf.d/docker-clean; \
    echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache;
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update \
    && apt-get install -y gettext binutils libproj-dev gdal-bin

RUN pip install playwright
RUN playwright install-deps chromium

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
RUN mkdir /code
WORKDIR /code
COPY requirements /code/requirements
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements/base.txt

RUN playwright install chromium

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements/deploy.txt

COPY .ssh /root/.ssh
COPY . /code/

COPY --from=build-lazer /code/lazer_app/projectLazer/www /code/static/lazer

RUN \
    DJANGO_SECRET_KEY=deadbeefcafe \
    DATABASE_URL=None \
    RECAPTCHA_PRIVATE_KEY=None \
    RECAPTCHA_PUBLIC_KEY=None \
    DJANGO_SETTINGS_MODULE=pbaabp.settings \
    python manage.py collectstatic --noinput
