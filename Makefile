.EXPORT_ALL_VARIABLES:

# CONFIGURATION
VENV_NAME=.venv
# make pipenv create local venv
PIPENV_VENV_IN_PROJECT=true

$(VENV_NAME):
	pipenv install -d
	pipenv run python -m spacy download nl_core_news_sm

test: $(VENV_NAME)
	pipenv run pytest tests/ -vv --ff

clean:
	pipenv --rm

