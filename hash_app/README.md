# Hash Table Analyzer — Flask Web App

A portfolio web application that visualizes hash table behavior using your `hashing_core.py` logic.

## Project Structure

```
hash_app/
├── app.py               # Flask backend
├── hashing_core.py      # Your original hash table logic
├── words.txt            # Word list (place here)
├── requirements.txt     # Python dependencies
├── static/
│   └── style.css        # Stylesheet
└── templates/
    ├── index.html       # Landing page
    └── dashboard.html   # Dashboard with stats + search
```

## Setup & Run

### 1. Install Flask

```bash
pip install flask
```

### 2. Place your words.txt

Make sure `words.txt` is in the same folder as `app.py`.

### 3. Run the app

```bash
python app.py
```

Then open your browser and go to: **http://127.0.0.1:5000**

## How It Works

1. **Homepage** — click "Build Hash Tables"
2. **Dashboard** — all 12 tables are built and stats are shown
3. **Search** — type a word, see found/not found + timing for every table
4. **Best result** is highlighted with timing in microseconds

## Features

- Load factor progress bars (green/yellow/red by fill level)
- Per-table statistics: collisions, filled slots, empty slots
- Real-time search across all 12 tables
- Fastest result highlighted
- Rebuild button to re-read words.txt fresh
