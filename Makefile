RAW_DIR := raws

# Define the publish target
publish: $(patsubst $(RAW_DIR)/%,%,$(wildcard $(RAW_DIR)/*))
	@echo "Publishing completed."

# Pattern rule to specify how to build each file
%: $(RAW_DIR)/%
	@echo "Processing $<"
	python3 ./manage.py --file_path "$<"

# Install dependencies
deps:
	python3 -m pip install -U pip
	python3 -m pip install -U click logzero nicegui pathlib
	python3 -m pipx install black

# Launch the website
serve:
	python3 ./web/main.py
