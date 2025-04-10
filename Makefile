check:
	flake8 .

extract:
	pybabel extract --input-dirs=. -o locales/messages.pot

init:
	pybabel init -i locales/messages.pot -d locales  -l en
	pybabel init -i locales/messages.pot -d locales  -l uz

compile:
	pybabel compile -d locales

update:
	pybabel update -d locales -i locales/messages.pot

create_migrate:
	alembic init migrations

create_async_migrate:
	alembic init -t async alembic

makemigrations:
	alembic revision --autogenerate -m "Initial migration"

migrate:
	alembic upgrade head

down_migrate:
	alembic downgrade -1