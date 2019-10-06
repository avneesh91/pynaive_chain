format-code: 
	yapf . -r -i

unit-tests:
	pytest . --verbose

debug-unit-tests:
	pytest -s . --verbose
