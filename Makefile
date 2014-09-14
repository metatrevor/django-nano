
clean:
	-rm -rf build
	-rm -rf dist
	-rm -rf nano.egg-info
	-find . -name '*.pyc' -exec rm -rf {} \;
	-find . -type d -empty -exec rmdir {} \;
