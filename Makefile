run:
	poetry run uvicorn main:app --reload

migrations:
	poetry run alembic init migrations

revision:
	poetry run alembic revision --autogenerate

upgrade:
	poetry run alembic upgrade head

lint:
	poetry run flake8 audio data users

test:
	poetry run pytest -v -s