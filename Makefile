lint:
	-ruff . --fix

fmt:
	isort . && black .

.PHONY: lint fmt