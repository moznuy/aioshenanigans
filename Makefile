.PHONY: build
build: clean
	python -m build

.PHONY: test-push
test-push:
	python -m twine upload --repository testpypi dist/*

.PHONY: push
push: build
	python -m twine upload --repository aioshenanigans dist/*

.PHONY: clean
clean:
	rm -rv ./dist/* || true
	rm -rv ./src/*.egg-info || true
