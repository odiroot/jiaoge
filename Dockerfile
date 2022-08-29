### BUILD STAGE ###
FROM python:3.10-alpine AS builder

WORKDIR /app
	
ARG BUILD_DEPS="postgresql-dev gcc python3-dev musl-dev libffi-dev libressl-dev zlib-dev jpeg-dev libjpeg"

RUN apk add --no-cache ${BUILD_DEPS} \
    && python -m venv .venv \
    && .venv/bin/pip install --no-cache-dir -U pip setuptools wheel

COPY requirements.txt .

RUN .venv/bin/pip install --no-cache-dir -r requirements.txt \
    && find /app/.venv \
	    \( -type d -a -name test -o -name tests \) \	
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' \+

### RUN STAGE ###
FROM python:3.10-alpine

WORKDIR /app

# No stdout buffering.
ENV PYTHONUNBUFFERED 1
# No pyc file writing
ENV PYTHONDONTWRITEBYTECODE 1

ARG RUNTIME_DEPS="libpq libffi libressl gettext icu-data-full zlib libjpeg"
RUN apk add --no-cache ${RUNTIME_DEPS}

COPY --from=builder /app /app
COPY . /app

# Make venv bins accessible.
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8080

CMD ["gunicorn", "jiaoge.wsgi:application", "--bind", ":8080", "--workers", "2",  "--access-logfile", "-"]

