# Makefile pour le projet Spotify ETL
# Jules Delrieu - Delight - Alternance

# Variables
IMAGE_NAME=spotify-etl
NOTEBOOK_PORT=8888
NOTEBOOK_DIR=$(PWD)/notebooks
DATA_DIR=$(PWD)/data

.PHONY: help build run-etl run-etl-debug notebook clean

# Affiche l'aide
help:
	@echo "Commandes disponibles :"
	@echo "  make build           - Construit l'image Docker"
	@echo "  make run-etl         - Lance le script ETL dans Docker"
	@echo "  make notebook        - Lance Jupyter Notebook dans Docker"
	@echo "  make clean           - Supprime l'image Docker locale"

# Construit l'image Docker
build:
	docker build -t $(IMAGE_NAME) .

# Lance le script ETL complet
run-etl:
	docker run --rm -v $(DATA_DIR):/app/data $(IMAGE_NAME)

# Lance Jupyter notebook à l'intérieur du conteneur
notebook:
	docker run --rm -it \
		-p $(NOTEBOOK_PORT):8888 \
		-v $(PWD):/app \
		-w /app \
		$(IMAGE_NAME) \
		jupyter notebook --ip=0.0.0.0 --no-browser --NotebookApp.token='' --NotebookApp.password=''

# Lance les tests Pytest dans Docker
test:
	docker run --rm \
		-v $(PWD):/app \
		-w /app \
		$(IMAGE_NAME) \
		pytest tests/


# Supprime l'image docker locale
clean:
	docker rmi -f $(IMAGE_NAME) || true
