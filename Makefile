RAW_DIR := raws
ARTICLES_DIR := web/articles
PYTHON := python3

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
	$(PYTHON) -m pip install -U click feedgen nbconvert nicegui openai pathlib
	$(PYTHON) -m pip freeze | grep -E "click|feedgen|nbconvert|nicegui|pathlib" > requirements.txt

# Launch the website
serve:
	$(PYTHON) ./web/main.py

# Proofreading using ChatGPT
review:
	@echo "Proofreading the latest article..."
	@$(PYTHON) ./review.py $(ARTICLES_DIR)/$(shell ls -1 -t $(ARTICLES_DIR) | tail -1)

.PHONY: publish deps serve review
