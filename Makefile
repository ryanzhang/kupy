.ONESHELL:
ENV_PREFIX=$(shell python3 -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")
USING_POETRY=$(shell grep "tool.poetry" pyproject.toml && echo "yes")

.PHONY: help
help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep


.PHONY: show
show:             ## Show the current environment.
	@echo "Current environment:"
	@if [ "$(USING_POETRY)" ]; then poetry env info && exit; fi
	@echo "Running using $(ENV_PREFIX)"
	@$(ENV_PREFIX)python -V
	@$(ENV_PREFIX)python -m site

.PHONY: install
install:          ## Install the project in dev mode.
	@if [ "$(USING_POETRY)" ]; then poetry install && exit; fi
	@echo "Don't forget to run 'make virtualenv' if you got errors."
	$(ENV_PREFIX)pip install -e .[test]

.PHONY: fmt
fmt:              ## Format code using black & isort.
	$(ENV_PREFIX)isort kupy/
	$(ENV_PREFIX)black -l 79 kupy/
	$(ENV_PREFIX)black -l 79 tests/

.PHONY: lint
lint:             ## Run pep8, black, mypy linters.
	$(ENV_PREFIX)flake8 kupy/
	$(ENV_PREFIX)black -l 79 --check kupy/
	$(ENV_PREFIX)black -l 79 --check tests/
	$(ENV_PREFIX)mypy --ignore-missing-imports kupy/

.PHONY: test
test: lint        ## Run tests and generate coverage report.
	$(ENV_PREFIX)pytest -v --cov-config .coveragerc --cov=kupy -l --tb=short --maxfail=1 tests/ || exit 1
	$(ENV_PREFIX)coverage xml
	# $(ENV_PREFIX)coverage html

.PHONY: watch
watch:            ## Run tests on every change.
	ls **/**.py | entr $(ENV_PREFIX)pytest -s -vvv -l --tb=long --maxfail=1 tests/

.PHONY: clean
clean:            ## Clean unused files.
	-find ./ -name '*.pyc' -exec rm -f {} \;
	-find ./ -name '__pycache__' -exec rm -rf {} \;
	-find ./ -name 'Thumbs.db' -exec rm -f {} \;
	-find ./ -name '*~' -exec rm -f {} \;
	-rm -rf .cache
	-rm -rf .pytest_cache
	-rm -rf .mypy_cache
	-rm -rf build
	-rm -rf dist
	-rm -rf *.egg-info
	-rm -rf htmlcov
	-rm -rf .tox/
	-rm -rf docs/_build

.PHONY: virtualenv
virtualenv:       ## Create a virtual environment.
	@if [ "$(USING_POETRY)" ]; then poetry install && exit; fi
	@echo "creating virtualenv ..."
	@rm -rf .venv
	@python3 -m venv .venv
	@./.venv/bin/pip install -U pip
	@./.venv/bin/pip install -e .[test]
	@echo
	@echo "!!! Please run 'source .venv/bin/activate' to enable the environment !!!"

.PHONY: release
release:          ## Create a new tag for release.
	@$(ENV_PREFIX)gitchangelog > HISTORY.md
	@TAG=$(shell cat kupy/VERSION|sed "s/.1dev//");\
	sed -i "s=unreleased=$${TAG}=g" HISTORY.md||True;\
	git add kupy/VERSION HISTORY.md;\
	git commit -m "release: version $${TAG} 🚀";\
	echo "creating git tag : v$${TAG}";\
	git tag v$${TAG} ;\
	echo $${TAG}.1dev > kupy/VERSION;\
	git add kupy/VERSION;\
	git commit -m "Pump version up $${TAG}.dev";
	@git push -u origin HEAD --tags
	@git push -u origin HEAD 
	@echo "Github Actions will detect the new tag and release the new version."

.PHONY: docs
docs:             ## Build the documentation.
	@echo "building documentation ..."
	@$(ENV_PREFIX)mkdocs build
	URL="site/index.html"; xdg-open $$URL || sensible-browser $$URL || x-www-browser $$URL || gnome-open $$URL

.PHONY: switch-to-poetry
switch-to-poetry: ## Switch to poetry package manager.
	@echo "Switching to poetry ..."
	@if ! poetry --version > /dev/null; then echo 'poetry is required, install from https://python-poetry.org/'; exit 1; fi
	@rm -rf .venv
	@poetry init --no-interaction --name=a_flask_test --author=rochacbruno
	@echo "" >> pyproject.toml
	@echo "[tool.poetry.scripts]" >> pyproject.toml
	@echo "kupy = 'kupy.__main__:main'" >> pyproject.toml
	@cat requirements.txt | while read in; do poetry add --no-interaction "$${in}"; done
	@cat requirements-test.txt | while read in; do poetry add --no-interaction "$${in}" --dev; done
	@poetry install --no-interaction
	@mkdir -p .github/backup
	@mv requirements* .github/backup
	@mv setup.py .github/backup
	@echo "You have switched to https://python-poetry.org/ package manager."
	@echo "Please run 'poetry shell' or 'poetry run kupy'"

.PHONY: init
init:             ## Initialize the project based on an application template.
	@./.github/init.sh

.PHONY: testdist stagedeploy systest sdist

sdist: clean test testdist systest

testdist: clean
	@git checkout kupy/VERSION
	@PRE_TAG=$(shell cat kupy/VERSION|sed "s/.1dev//");\
	read -p "Version? (provide the next x.y.z version,Previous tag, $${PRE_TAG} ) : " TAG;\
	echo $$TAG > kupy/VERSION;\
	python setup.py sdist bdist_wheel
	twine upload -r pypitest dist/*

systest:
	#Wait 30 seconds for test.pypi.org to proceed
	@sleep 30
	cd systest && make test
	

.PHONY: dist
# sdist:
dist: release
	# python setup.py sdist bdist_wheel
	twine upload -r pypi dist/*
	

# This project has been generated from ryanzhang/python-project-template which is forked from 
# rochacbruno/python-project-template
# original template __author__ = 'rochacbruno'
# __repo__ = https://github.com/rochacbruno/python-project-template
# __sponsor__ = https://github.com/sponsors/rochacbruno/
