TEST_CMD = python3 -m doctest
CHECKSTYLE_CMD = flake8

all: test checkstyle

test:
	$(TEST_CMD) *.py

checkstyle:
	$(CHECKSTYLE_CMD) *.py

clean:
	rm -f *.pyc
	rm -rf __pycache__
