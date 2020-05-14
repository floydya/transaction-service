FROM python:alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev libffi-dev make libpq

RUN pip install pipenv
COPY Pipfile* /app/
RUN pipenv install --system --dev

COPY . /app/

CMD chmod +x /app/entrypoint.sh

EXPOSE 80
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
