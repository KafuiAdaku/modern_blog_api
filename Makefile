# Command to build Docker containers defined in development.yml
build:
	docker compose -f development.yml up --build --remove-orphans

# Command to start Docker containers defined in development.yml
up:
	docker compose -f development.yml up

# Command to stop and remove Docker containers defined in development.yml
down:
	docker compose -f development.yml down

# Command to display logs of Docker containers defined in development.yml
show_logs:
	docker compose -f development.yml logs

# Command to run Django database migrations in the api service container
migrate:
	docker compose -f development.yml run --rm api python3 manage.py migrate

# Command to create Django database migration files based on changes in models
makemigrations:
	docker compose -f development.yml run --rm api python3 manage.py makemigrations

# Command to collect static files into STATIC_ROOT directory
collectstatic:
	docker compose -f development.yml run --rm api python3 manage.py collectstatic --no-input --clear

# Command to create a superuser in the Django application
superuser:
	docker compose -f development.yml run --rm api python3 manage.py createsuperuser

# Command to stop and remove Docker containers as well as associated volumes
down-v:
	docker compose -f development.yml down -v

# Command to inspect a Docker volume named modern-blog-src_development_postgres_data
volume:
	docker volume inspect modern-blog-src_development_postgres_data

# Command to execute psql commands against PostgreSQL database container
modern-blog-db:
	docker compose -f development.yml exec postgres psql --username=modernblog --dbname=modern-blog-db

# Command to run flake8 tool for linting Python code
flake8:
	docker compose -f development.yml exec api flake8 .

# Command to check compliance with Black code style
black-check:
	docker compose -f development.yml exec api black --check --exclude=migrations .

# Command to show differences after applying Black formatting to Python files
black-diff:
	docker compose -f development.yml exec api black --diff --exclude=migrations .

# Command to format Python files according to Black code style
black:
	docker compose -f development.yml exec api black --exclude=migrations .

# Command to check import sorting in Python files using isort
isort-check:
	docker compose -f development.yml exec api isort . --check-only --skip env --skip migrations

# Command to show differences after applying isort import sorting to Python files
isort-diff:
	docker compose -f development.yml exec api isort . --diff --skip env --skip migrations

# Command to apply import sorting to Python files using isort
isort:
	docker compose -f development.yml exec api isort . --skip env --skip migration

# Command to check environment variables of Django app
check-env:
	docker compose -f development.yml run --rm api python check_env.py

# command to rebuild search index
search_index:
	docker compose -f development.yml run --rm api python manage.py rebuild_index

# Command to check Django project for common problems and inconsistencies
check:
	docker compose -f development.yml run --rm api python3 manage.py check
