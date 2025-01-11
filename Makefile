push:
	git push origin master

submit:
	git push submit semestral

dependencies:
	pip freeze > requirements.txt

run:
	python src/game_of_life/app.py

cli:
	python src/game_of_life/cli_game.py

.PHONY: push submit dependencies run cli
