FROM python:3.11-slim

# Crée un utilisateur non-root
RUN useradd -ms /bin/bash jupyteruser

WORKDIR /home/jupyteruser/app

# Dépendances pour certaines lib python (ex: pandas)
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copie les requirements
COPY requirements.txt .

# Installe les libs Python + jupyter
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir notebook ipykernel jupyterlab

# Copie le reste du projet
COPY . .

USER jupyteruser

EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--NotebookApp.token=''", "--NotebookApp.password=''"]
