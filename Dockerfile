### BUILD STAGE ###
FROM python:3.7-alpine AS builder

WORKDIR /app
	
ARG BUILD_DEPS="postgresql-dev gcc python-dev musl-dev libffi-dev libressl-dev"

RUN apk add --no-cache ${BUILD_DEPS} \
    && python -m venv .venv \
    && .venv/bin/pip install --no-cache-dir -U pip setuptools

COPY requirements.txt .

RUN .venv/bin/pip install --no-cache-dir -r requirements.txt \
    && find /app/.venv \
	    \( -type d -a -name test -o -name tests \) \	
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' \+

### RUN STAGE ###
FROM python:3.7-alpine

WORKDIR /app

# No stdout buffering.
ENV PYTHONUNBUFFERED 1
# No pyc file writing
ENV PYTHONDONTWRITEBYTECODE 1

ARG RUNTIME_DEPS="libpq libffi libressl"	
RUN apk add --no-cache ${RUNTIME_DEPS}

COPY --from=builder /app /app
COPY jiaoge jiaoge
COPY manage.py .

# Make venv bins accessible.
ENV PATH="/app/.venv/bin:$PATH"

CMD ["gunicorn", "jiaoge.wsgi:application", "--bind", "0.0.0.0:8000", "--access-logfile", "-"]

