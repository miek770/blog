RAW_DIR := raws
ARTICLES_DIR := web/articles

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
	@echo "Processing $<..."Running command on
	$(PYTHON) ./manage.py --file_path "$<"

# Install dependencies
# I always want the latest version of each library, but I want to pin my dependencies
# to get warnings from GitHub if there's a security issue.
deps:
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -U black[jupyter] click feedgen nbconvert nicegui openai pathlib pre-commit dataset
	$(PYTHON) -m pip freeze | grep -E "black|click|feedgen|nbconvert|nicegui|openai|pathlib|pre-commit|dataset" > requirements.txt
	$(PYTHON) -m pre-commit install
	$(PYTHON) -m pre-commit run --all-files

# pre-commit autoupdate (not sure if should be included)
# https://pre-commit.com/#updating-hooks-automatically

# Launch the website
serve:
	$(PYTHON) ./web/main.py

# Proofreading using ChatGPT
review:
	@echo "Proofreading the latest article..."
	$(PYTHON) ./review.py $(ARTICLES_DIR)/$(shell ls -1 $(ARTICLES_DIR) | tail -1)

.PHONY: publish deps serve review
