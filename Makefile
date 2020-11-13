.EXPORT_ALL_VARIABLES:

# CONFIGURATION
VENV_NAME=.venv
# make poetry create local venv
POETRY_VIRTUALENVS_IN_PROJECT=true

.DEFAULT_GOAL := test

poetry.lock:
	poetry lock -vvv
	rm -rf $(VENV_NAME)

$(VENV_NAME): | poetry.lock
	poetry install -vvv
	poetry show --tree

pre-commit: $(VENV_NAME)
	poetry run pre-commit install

.PHONY: test
test: pre-commit
	poetry run pytest tests/ -vv --ff

.PHONY: update
update: pre-commit
	poetry update

.PHONY: clean
clean:
	rm -rf $(VENV_NAME)
	rm poetry.lock
