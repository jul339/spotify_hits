# 🎧 Spotify Top Hits ETL – Technical Test (Delight)

This project is a technical test completed as part of the recruitment process for a **Data Engineer (Python)** apprenticeship at **Delight**. It consists of building a modular Python ETL pipeline using the public Spotify API, along with data exploration in a Jupyter Notebook.

---

## 🚀 Project Objectives

- Extract data from Spotify playlists titled "Top Hits of YYYY" (from 2020 to 2024)
- Collect key information on both tracks and artists (popularity, followers, genres, duration, etc.)
- Store the data in a clean and reusable format (CSV)
- Explore and visualize the data to answer analytical questions

---

## 🛠️ Tech Stack

- **Language**: Python 3.11  
- **Libraries**: `spotipy`, `pandas`, `matplotlib`, `seaborn`, `pytest`  
- **Containerization**: Docker  
- **Testing**: Pytest (unit and functional tests)  
- **Structure**: Modular layout (`src/`, `tests/`, `notebooks/`)

---

## 📁 Project Structure

```
spotify_hits/
├── src/                # ETL logic and configuration
│   ├── etl.py
│   └── config.py
├── tests/              # Unit tests (pytest)
│   ├── test_etl.py
│   └── ...
├── notebooks/          # Data analysis (Jupyter)
│   └── exploration.ipynb
├── data/               # Raw and processed CSVs (excluded from Git)
├── Dockerfile          # Docker image definition
├── Makefile            # Commands for building, testing, running
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## ⚙️ Setup Without Docker

```bash
# Clone the repository
git clone https://github.com/your-username/spotify_hits.git
cd spotify_hits

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the ETL pipeline
python src/main.py
```

---

## 🐳 Docker Usage (Recommended)

### 1. Build the Docker image

```bash
make build
```

### 2. Run the full ETL

```bash
make run-etl
```

### 3. Launch Jupyter Notebook

```bash
make notebook
# Then open http://localhost:8888/ in your browser
```

### 4. Run unit tests

```bash
make test
```

---

## 📊 Data Exploration & Visualization

All analyses are available in [`notebooks/exploration.ipynb`](notebooks/exploration.ipynb), with charts and explanations answering:

- 📈 **Is artist popularity correlated with their follower count or track popularity?**
- 🎶 **How have the most popular genres evolved between 2020 and 2024?**
- ⏱️ **Has the average duration of hit tracks changed over the years?**
- 🧑‍🎤 **Which artists appeared the most across the 5 playlists?**
- 📈 Additional exploratory visualizations (distributions, correlations, etc.)

---


## 🔐 Spotify API Authentication

You need a Spotify Developer account:  
https://developer.spotify.com/dashboard

**Required environment variables** (store in a local `.env` file, not committed):

```
SPOTIPY_CLIENT_ID=xxxxxxxxxxxx
SPOTIPY_CLIENT_SECRET=xxxxxxxxxxxx
```

These credentials are injected via `spotipy`’s client credentials flow.

---

## 🙋 Author

**Jules Delrieu**  

---
