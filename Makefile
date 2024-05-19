test-all:
	@pytest

update-requirements:
	@pip freeze > requirements.txt

set-pythonpath:
	@export PYTHONPATH=/home/ivan/Documents/catland_planilha:$PYTHONPATH && echo "PYTHONPATH set to: $$PYTHONPATH"

run-main:
	@python src/main.py