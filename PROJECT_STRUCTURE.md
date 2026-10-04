# Project Structure Guide

This document explains how the current workshop files fit together. It reflects the repository as it exists now.

## Repository map

```text
movie-recs-workshop/
├── .github/workflows/ci.yml
├── data/
│   ├── README.md
│   └── movies.json
├── tests/
│   ├── test_advanced_recommender.py
│   └── test_recommender.py
├── .env.example
├── .gitignore
├── README.md
├── START_HERE.md
├── PROJECT_STRUCTURE.md
├── recommender.py
├── advanced_recommender.py
├── setup_api_key.py
├── requirements.txt
└── requirements-advanced.txt
```

## Core scripts

### `recommender.py`

The beginner workshop application.

It demonstrates:

- reading user input
- normalizing comma-separated tags
- loading JSON data
- mapping mood words to TMDB genres
- making optional HTTP requests
- handling request and JSON errors
- deterministic recommendation scoring
- graceful local fallback behavior

The local recommendation algorithm is intentionally simple:

1. Convert the user's input into lowercase tags.
2. Compare those tags with each movie's `mood_tags`.
3. Award points for tag overlap.
4. Add a small bonus when the main genre directly matches.
5. Rank positive-scoring movies and return the top matches.

This makes the recommendation logic easy for beginners to inspect and modify.

### `advanced_recommender.py`

The advanced extension uses MovieLens user ratings for item-item collaborative filtering.

It demonstrates:

- loading tabular rating data
- filtering movies with enough ratings
- representing movies by user-rating vectors
- cosine similarity
- fuzzy title matching
- recommendation ranking

The script has two execution paths:

- **pandas/scikit-learn path** — builds a movie × user matrix and computes a cosine-similarity matrix.
- **pure-Python path** — represents movie vectors as dictionaries and calculates sparse cosine similarity manually.

The fallback path keeps the algorithm inspectable and allows the learning exercise to continue even if data-science packages are unavailable.

### `setup_api_key.py`

Optional helper for live TMDB access.

It:

- opens the TMDB API settings page
- accepts the key with hidden terminal input
- stores it in the project `.env` file
- preserves unrelated `.env` entries

The beginner recommender still works without this script because local data is the default fallback.

## Data

### `data/movies.json`

A small local teaching dataset used by the beginner recommender.

It exists so the workshop can run without:

- an external API account
- internet access
- a large dataset

The file is intentionally small enough for students to open and understand directly.

### `data/ml-latest-small/`

Created locally by the student when they download the MovieLens Latest Small dataset.

At minimum, the advanced script expects:

```text
movies.csv
ratings.csv
```

Downloaded MovieLens files are ignored by Git. See `data/README.md` for source and license notes.

## Configuration

### `.env.example`

Safe template showing the expected environment variable:

```text
TMDB_API_KEY=your_tmdb_api_key_here
```

Students copy it to `.env` only if they want the live API extension.

### `.gitignore`

Protects local secrets, virtual environments, caches, downloaded MovieLens data, editor files, and build artifacts from accidental commits.

## Dependencies

### `requirements.txt`

Beginner path:

- `requests`
- `python-dotenv`

### `requirements-advanced.txt`

Adds the data-science stack needed for the preferred collaborative-filtering path.

## Tests

The `tests/` folder validates logic that can be checked without an API key or network connection.

That includes:

- tag parsing
- TMDB genre mapping
- deterministic ranking
- sparse cosine similarity
- fuzzy title matching
- pure-Python recommendation generation

## CI

`.github/workflows/ci.yml` runs syntax checks and the unit-test suite on pushes and pull requests.

The CI intentionally avoids calling TMDB so repository validation does not depend on external credentials or network availability.

## Execution flow

### Beginner path

```text
user input
   ↓
parse tags
   ↓
TMDB configured? ── yes ──→ request live movies
   │                           │
   no                          │ failure
   ↓                           ↓
load local JSON ←──────────────┘
   ↓
score tag overlap
   ↓
rank recommendations
   ↓
print results
```

### Advanced path

```text
MovieLens movies + ratings
          ↓
filter movies with enough ratings
          ↓
build movie rating vectors
          ↓
cosine similarity
          ↓
match user's movie title
          ↓
rank similar movies
          ↓
print recommendations
```

## Design goal

The project is intentionally progressive. Students can stop after the local Python exercise, continue into API integration, or go further into collaborative filtering without needing three separate repositories.
