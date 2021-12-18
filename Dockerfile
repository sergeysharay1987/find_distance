FROM python:3.7.0-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR usr/src/app
COPY pyproject.toml .
COPY poetry.lock .
RUN pip install --upgrade pip && pip install poetry && poetry install
EXPOSE 5000
COPY . .
CMD ["poetry", "run", "python", "-m", "main"]
