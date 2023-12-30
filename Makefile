.PHONY: tests install run

run:
	python -m linkedin_crawler --help

install:
	pip install -e .

tests:
	python -m pytest tests --cov=./linkedin_crawler
