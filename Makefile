test-all:
	@pytest

update-requirements:
	@pip freeze > requirements.txt