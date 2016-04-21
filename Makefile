.PHONY: test
test: test_python3 test_python2

.PHONY: test_python3
test_python3:
	python3 -m unittest discover -s tests/ -p 'test_*.py'

.PHONY: test_python2
test_python2:
	python2.7 -m unittest discover -s tests/ -p 'test_*.py'

.PHONY: coverage
coverage:
	coverage run --source=botutil -m unittest discover -s tests
	coverage report -m
	coverage html
