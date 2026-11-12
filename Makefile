install:
	@echo "Project has no dependencies"

run:
	python3 a_maze_ing.py config.txt

debug:
	python3 -m pdb a_maze_ing.py config.txt

clean:
	rm -rf **/.mypy_cache
	rm -rf **/__pycache__

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-def --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
