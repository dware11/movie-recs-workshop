# Start Here — Fast Workshop Setup

Use this guide when you want the beginner version running with the least setup.

## 1. Open the repository

Open the `movie-recs-workshop` folder in your editor.

## 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

## 3. Install beginner dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the local recommender

```bash
python recommender.py
```

If `python` is not recognized on Windows, try:

```bash
py recommender.py
```

## 5. Enter a few vibe words

Examples:

- `chill, funny`
- `action, adventure`
- `cozy, feel-good`

The beginner version works from `data/movies.json`, so an API key is not required.

## Optional: enable live TMDB data

```bash
python setup_api_key.py
```

Then run `python recommender.py` again. If TMDB is unavailable, the project safely falls back to the local dataset.

## Optional: try collaborative filtering

See the **Advanced path** in `README.md`. That extension uses MovieLens ratings and `advanced_recommender.py`.
