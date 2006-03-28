all: test doc
	@echo "If the tests pass and the docs are created you should be fine" 


doc: 
	@make -C docs docs
	@python setup.py doc


dist: 
	@python setup.py bdist_egg
test: 
	@python tests/runalltests.py

clean: 
	@find . -name "*.pyc" -exec rm {} \;
	@find . -name "*~" -exec rm {} \;
	@rm -rf *.egg-info
	@${MAKE} -C docs clean
