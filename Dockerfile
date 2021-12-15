FROM python:3.9.2-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR usr/src/app
COPY pyproject.toml .
COPY poetry.lock .
RUN pip install poetry && poetry install
EXPOSE 5000
COPY . .
CMD ["poetry", "run", "python", "-m", "main"]
