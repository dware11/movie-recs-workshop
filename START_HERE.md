# Start Here: Fast Workshop Setup

Use this quick guide if you want to run the project in under 2 minutes.

## 1) Open this folder in Cursor
- Open Cursor
- Click "Open Folder"
- Select `movie-recs-workshop`

## 2) Install dependencies

```bash
pip install -r requirements.txt
```

## 3) Run the basic workshop version

```bash
python recommender.py
```

If `python` does not work on Windows:

```bash
py recommender.py
```

## 4) Enter your vibe words
Examples:
- `chill, funny`
- `action, adventure`
- `cozy, feel-good`

## Optional: Live API version
If you want live TMDB data later, run:

```bash
python setup_api_key.py
```

Then run `python recommender.py` again.

For full beginner instructions (basic + advanced paths), open `README.md`.
