
clean:
	-find . -name '*.pyc' -exec rm -rf {} \;
	-find . -type d -empty -exec rmdir {} \;
	-rm -rf build
	-rm -rf dist
	-rm -rf nano.egg-info
