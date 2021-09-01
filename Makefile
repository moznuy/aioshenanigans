.PHONY: build

build: clean
	python -m build

test-push:
	python -m twine upload --repository testpypi dist/*

push:
	python -m twine upload --repository pypi dist/*

clean:
	rm -rv ./dist/* || true
	rm -rv ./src/*.egg-info || true
