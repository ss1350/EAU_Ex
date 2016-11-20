PYTHON_CMD = python3
TEST_CMD = $(PYTHON_CMD) -m doctest
CHECKSTYLE_CMD = flake8

all: compile test checkstyle run

compile:
	@echo "Nothing to compile for Python"

test:
	$(TEST_CMD) *.py

checkstyle:
	$(CHECKSTYLE_CMD) *.py --show-source

clean:
	rm -f *.pyc
	rm -rf __pycache__

run:
	$(PYTHON_CMD) Ex1.py