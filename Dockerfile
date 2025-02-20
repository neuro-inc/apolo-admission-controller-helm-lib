FROM python:3.12-slim-bullseye

WORKDIR /app

ADD pyproject.toml /app

# You likely need 'cryptography' and 'kubernetes' if you do K8s API calls
RUN pip install poetry==2.1.1
RUN poetry config virtualenvs.create false
RUN poetry install

ADD hooks /app/hooks

ENTRYPOINT ["python", "-m", "hooks"]