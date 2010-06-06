all: check_dependencies test

filename=dominic-`python -c 'import dominic;print dominic.version'`.tar.gz

export PYTHONPATH:=  ${PYTHONPATH}:${PWD}

check_dependencies:
	@echo "Checking for dependencies to run tests ..."
	@python -c "import sure" 2>/dev/null || (echo "You must install sure in order to run dominic's tests" && exit 3)
	@python -c "import xpath" 2>/dev/null || (echo "You must install py-dom-xpath in order to run dominic's tests" && exit 3)

test: clean
	@echo "Running dominic tests ..."
	@nosetests -s --verbosity=2 --with-coverage --cover-erase --cover-inclusive ./tests/ --cover-package=dominic

doctest: clean
	@cd docs && make doctest

documentation:
	@cd docs && make html

clean:
	@printf "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do rm -rf $$pattern; find . -name "$$pattern" -exec rm -rf {} \;; done
	@echo "OK!"

release: clean
	@printf "Exporting to $(filename)... "
	@tar czf $(filename) dominic setup.py README.md COPYING
	@echo "DONE!"
