all: docs

docs: walkthrough.rst style.css
	@rst2html --stylesheet-path=style.css walkthrough.rst > walkthrough.html

clean:
	@rm -f walkthrough.html

