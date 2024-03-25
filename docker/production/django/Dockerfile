# Stage 1: Build Stage
ARG PYTHON_VERSION=3.9-slim-bullseye
FROM python:${PYTHON_VERSION} as python

FROM python as python-build-stage
ARG BUILD_ENVIRONMENT=production

# Install build dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev

# Copy requirements files to the build stage
COPY ./requirements .

# Use pip to create wheel packages and store them in /usr/src/app/wheels
RUN pip wheel --wheel-dir /usr/src/app/wheels \
    -r ${BUILD_ENVIRONMENT}.txt

# Stage 2: Run Stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=production
ARG APP_HOME=/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

# Set working directory
WORKDIR ${APP_HOME}

# Creating a user in django to override the default root user
RUN addgroup --system modernblogapi \
    && adduser --system --ingroup modernblogapi modernblogapi

# Install runtime dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext netcat \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Copy wheel packages from the build stage to the runtime stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels/

# Install dependencies from the wheel packages
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
   && rm -rf /wheels/

# Copy entrypoint and start scripts
COPY --chown=modernblogapi:modernblogapi ./docker/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY --chown=modernblogapi:modernblogapi ./docker/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY --chown=modernblogapi:modernblogapi ./docker/production/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./docker/production/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

# Copy application code
COPY --chown=modernblogapi:modernblogapi . ${APP_HOME}

# Make modernblogapi user the user of the dir
RUN chown modernblogapi:modernblogapi ${APP_HOME}

# switch to new user
USER modernblogapi

# Define the entrypoint for the container
ENTRYPOINT ["/entrypoint"]