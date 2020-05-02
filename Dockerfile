#FROM python:slim
#
#RUN addgroup -S app && adduser -S app -G app
#RUN mkdir -p /src
#ENV APP_DIR=/src
#WORKDIR $APP_DIR
#
#RUN apk update && apk add postgresql-dev gcc python3-dev libpq-dev
#
#RUN pip install --upgrade pip
#RUN pip install pipenv
#COPY ./Pipfile* $APP_DIR/
#RUN pipenv install --system --dev --ignore-pipfile
#
#COPY . $APP_DIR/
#RUN chown -R app:app $APP_DIR
#
#USER app


FROM python:alpine as base

FROM base as builder

RUN mkdir /install
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev libffi-dev make
RUN pip install pipenv
WORKDIR /install

COPY Pipfile ./Pipfile
RUN pipenv lock -r > requirements.txt

RUN pip install --install-option="--prefix=/install" -r ./requirements.txt

FROM base

COPY --from=builder /install /usr/local
COPY .  /app
RUN apk --no-cache add libpq
WORKDIR /app
