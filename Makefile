# Makefile for project automation

# Define targets
.PHONY: install run

# Target to install project dependencies
install:
	pip install -r requirements.txt

test:
	pytest -v

trulens:
	python platforms/trulens/run.py $(filter-out $@,$(MAKECMDGOALS))
%: ; @:

run:
	streamlit run src/chatbot/streamlit.py

# Default target
.DEFAULT_GOAL := test