format-code: 
	yapf . -r -i

test: unit-tests integration-tests

unit-tests:
	pytest unit_tests/ --verbose

debug-unit-tests:
	pytest -s unit_tests/ --verbose

integration-tests:
	pytest integration_tests/ --verbose

debug-integration-tests:
	pytest -s integration_tests/ --verbose


