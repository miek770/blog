RAW_DIR := raws

# Determine the operating system
ifeq ($(OS),Windows_NT)
	# Windows
	PYTHON := py
else
	# Linux
	PYTHON := python3
endif

# Define the publish target
publish: $(patsubst $(RAW_DIR)/%,%,$(wildcard $(RAW_DIR)/*))
	@echo "Publishing completed."

# Pattern rule to specify how to build each file
%: $(RAW_DIR)/%
	@echo "Processing $<"
	$(PYTHON) ./manage.py --file_path "$<"

# Install dependencies
deps:
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -U click logzero nicegui pathlib pipx
	$(PYTHON) -m pipx install black

# Launch the website
serve:
	$(PYTHON) ./web/main.py
