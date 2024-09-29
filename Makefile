RAW_DIR := raws
ARTICLES_DIR := web/articles

# Define the publish target
publish: $(patsubst $(RAW_DIR)/%,%,$(wildcard $(RAW_DIR)/*))
	@echo "Publishing completed."
	@poetry run python ./rss.py
	@echo "RSS feed update completed."

# Pattern rule to specify how to build each file
%: $(RAW_DIR)/%
	@poetry run python ./manage.py --file_path "$<"

# Launch the website
serve:
	@poetry run python ./web/main.py

.PHONY: publish serve
