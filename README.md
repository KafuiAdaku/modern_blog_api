# MODERN BLOG API

![OS](https://img.shields.io/badge/OS-Linux-red?style=flat&logo=linux)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python%203.10-1f425f.svg?logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-available-green.svg?style=flat&logo=docker)](https://github.com/emalderson/ThePhish/tree/master/docker)
[![Maintenance](https://img.shields.io/badge/Maintained-yes-green.svg)](https://github.com/KafuiAdaku/FeedbackForm)
[![Documentation](https://img.shields.io/badge/Documentation-complete-green.svg?style=flat)](https://github.com/KafuiAdaku/FeedbackForm)

**A Django Rest Framework API for creating awesome blog post**

Swagger documentation for project API view routes is available at [https://www.modernblogapi.me/swagger/]

## Table of Contents

- [Project Overview](#project-overview)
- [Project Setup](#project-setup)
  - [Prerequisites](#prerequisites)
  - [Setting Up ModernBlog API](#setting-up-modernblog-api)
  - [Environment Configuration](#environment-configuration)
- [Build and Run](#build-and-run)
- [Testing](#testing)
  - [Running pytest](#running-pytest)
  - [Test Coverage](#test-coverage)
- [Initializing Database](#initializing-database)
- [Test With API Client](#test-with-api-client)
- [Contact](#contact)
- [License](#license)

## Project Overview

Modern Blog API is a versatile Django-powered backend application built with Django REST Framework, designed to emulate popular content-sharing platforms. This API provides robust functionality for managing blogs, user authentication, comments, and more. Whether you're building a front-end application or integrating with existing systems, Modern Blog API offers a flexible and extensible solution for your blogging needs

## Project Setup

### Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed `Docker` and `Docker Compose`.
- You have a suitable text editor to edit .env and other files.

## Setting Up ModernBlog Api

To install Modern Blog API, follow these steps:

1. Clone the repository.
2. Set up your environment variables in this path `.envs/.development/` :

### Environment Configuration

- Create a `.django` file in the project root `.envs/.development/` dir and set this variables:

```env
CELERY_BROKER=redis://redis:6379/0
CELERY_BACKEND=redis://redis:6379/0

DOMAIN=locahost:8080
EMAIL_PORT=1025

CELERY_FLOWER_USER=modern_blog_api
CELERY_FLOWER_PASSWORD="your-pass-word"

SIGNING_KEY="your-secret-key"
```

- Create a `.postgres` file in the same directory and set this variables:

```env
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB="your-postgres-db-name"
POSTGRES_USER="your-postgres-db-username"
POSTGRES_PASSWORD="your-postgres-db-password"
```

> These values will be used by the django settings file and in build your docker image

## To build a container from a docker compose file

```bash
make build
```

## Run a docker-compose after already building

> At the root of project directory run the following commands to build image

```bash
make up
```

## To create super user to access admin

```bash
make superuser
```

## To stop a running docker-compose app

```bash
make down
```

## To remove all created volumes

```bash
make down-v
```

> Check the `Makefile` at the root of the project directory for more make commands

# TESTING THE APP AND COVERAGE

## Checking for formatiing issues

```bash
make black-check
```

## Compare the changes to be made

```bash
make black-diff
```

## Make formatting changes

```bash
make black
```

## Check for sorting issues of imports

```bash
make isort-check
```

## Compare changes to be made if sorting issues are present

```bash
make isort-diff
```

## Makes sorting changes

```bash
make isort
```

## Check for Linting issues (pycodesytle)

```bash
make flake8
```
## Running pytest directly inside the docker container. Also gives test coverage report

```bash
pytest -p no:warnings --cov=. -v
```

# TEST WITH API CLIENT

Visit [localhost:8080/api/v1](http://localhost:8080/api/v1/) or [0.0.0.0:8080/api/v1](http://0.0.0.0:8080/api/v1/) and accompained views route in the swapper docs below

# Swagger View Routes for API

Visit [http://localhost:8080/swagger](http://localhost:8080/swagger) or [http://0.0.0.0:8080/swagger](http://localhost:8080/swagger)

## Contact

## Authors

- [Theophilus Ackom](https://github.com/TeamKweku)
- [Dennis Adaku](https://github.com/KafuiAdaku)

## License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for details.
