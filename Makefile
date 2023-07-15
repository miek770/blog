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
	$(PYTHON) ./rss.py
	@echo "RSS feed update completed."

# Pattern rule to specify how to build each file
%: $(RAW_DIR)/%
	@echo "Processing $<"
	$(PYTHON) ./manage.py --file_path "$<"

# Install dependencies
# I always want the latest version of each library, but I want to pin my dependencies
# to get warnings from GitHub if there's a security issue.
deps:
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -U click feedgen nbconvert nicegui pathlib
	$(PYTHON) -m pip freeze | grep -E "click|feedgen|nbconvert|nicegui|pathlib" > requirements.txt

# Launch the website
serve:
	$(PYTHON) ./web/main.py
