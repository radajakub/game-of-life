push:
	git push origin master

submit:
	git push submit semestral

dependencies:
	pip freeze > requirements.txt

run:
	python src/game_of_life/app.py

install:
	pip install -r requirements.txt
	pip install -e .

test:
	python -m pytest

.PHONY: push submit dependencies run install test
