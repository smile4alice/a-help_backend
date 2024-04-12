.PHONY: migrate-db, upgrade-db, initial-migration

init-db:
	if test -d migrations; then echo skipping; else flask db init; fi
migrate-db:	## create new migration
	flask db migrate
upgrade-db: ## upgrade target database with new migration
	flask db upgrade
start-develop: init-db migrate-db upgrade-db
	flask init
clean: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
