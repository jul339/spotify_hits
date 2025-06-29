FROM python:3.11-slim

RUN useradd -ms /bin/bash jupyteruser

WORKDIR /home/jupyteruser/app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir notebook ipykernel jupyterlab

COPY . .

USER jupyteruser

EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--NotebookApp.token=''", "--NotebookApp.password=''"]
