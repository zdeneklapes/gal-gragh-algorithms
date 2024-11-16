# Makefile for Docker Nginx PHP Composer MySQL

help: ## Show this help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {sub("\\\\n",sprintf("\n%22c"," "), $$2);printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

pack:
	zip -r xlapes02_xdvora3r.zip src/ Makefile README.md requirements.txt .python-version
