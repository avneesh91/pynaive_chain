test: format-code unit-tests integration-tests
pipeline: unit-tests integration-tests

format-code: 
	yapf . -r -i

unit-tests:
	pytest unit_tests/ --verbose

debug-unit-tests:
	pytest -s unit_tests/ --verbose

integration-tests:
	pytest integration_tests/ --verbose

debug-integration-tests:
	pytest -s integration_tests/ --verbose


