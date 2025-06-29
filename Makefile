IMAGE_NAME=spotify-etl
NOTEBOOK_PORT=8888
NOTEBOOK_DIR=$(PWD)/notebooks
DATA_DIR=$(PWD)/data

.PHONY: help build run-etl run-etl-debug notebook clean

help:
	@echo "Commandes disponibles :"
	@echo "  make build           - Construit l'image Docker"
	@echo "  make run-etl         - Lance le script ETL dans Docker"
	@echo "  make notebook        - Lance Jupyter Notebook dans Docker"
	@echo "  make test            - Exécute les tests avec pytest dans Docker"
	@echo "  make clean           - Supprime l'image Docker locale"

build:
	docker build -t $(IMAGE_NAME) .

# Run complet ETL script 
run-etl:
	docker run --rm -v $(DATA_DIR):/app/data $(IMAGE_NAME)

# Run jupiter notebook in Docker
notebook:
	docker run --rm -it \
		-p $(NOTEBOOK_PORT):8888 \
		-v $(PWD):/app \
		-w /app \
		$(IMAGE_NAME) \
		jupyter notebook --ip=0.0.0.0 --no-browser --NotebookApp.token='' --NotebookApp.password=''

# Run pytest tests
test:
	docker run --rm \
		-v $(PWD):/app \
		-w /app \
		$(IMAGE_NAME) \
		pytest tests/


# Delete docker image
clean:
	docker rmi -f $(IMAGE_NAME) || true
