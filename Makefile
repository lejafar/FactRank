.EXPORT_ALL_VARIABLES:

# CONFIGURATION
VENV_NAME=.venv
# make poetry create local venv
POETRY_VIRTUALENVS_IN_PROJECT=true

.DEFAULT: test

poetry.lock:
	poetry lock -vvv
	rm -rf $(VENV_NAME)

$(VENV_NAME): | poetry.lock
	poetry install -vvv
	poetry show --tree
	poetry run python -m spacy download nl_core_news_sm

.PHONY: test
test: $(VENV_NAME)
	poetry run pytest tests/ -vv --ff

.PHONY: update
update: $(VENV_NAME)
	poetry update

.PHONY: clean
clean:
	rm -rf $(VENV_NAME)
	rm poetry.lock

