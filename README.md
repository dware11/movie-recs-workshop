# AI Movie Recommender Workshop

This workshop project teaches beginner Python using a simple movie recommender.

The app has two modes:
- Basic version (recommended): local movie data, no API setup stress
- Live API version (optional): TMDB data for a more advanced extension

## Section A: Basic Version (Recommended for Beginners)

This is the safest path for class. Students can run the project without API setup.

### 1) Open the project in Cursor
1. Open Cursor
2. Select "Open Folder"
3. Choose this project folder: `movie-recs-workshop`

### 2) Install requirements
Use one command:

```bash
pip install -r requirements.txt
```

### 3) Run the recommender

```bash
python recommender.py
```

If `python` does not work on Windows, try:

```bash
py recommender.py
```

### 4) Enter a vibe
Try mood words like:
- `chill, funny`
- `action, adventure`
- `cozy, feel-good`

That is it. This basic version is enough for the core workshop.

## Section B: Live API Version (Advanced / Optional)

This optional version connects to TMDB (The Movie Database), a free movie data service.

Use this only after students are comfortable with the basic version.
If API setup feels confusing, skip this section and keep using the basic version.

### What the API key is for
An API key is like a password that lets your script ask TMDB for live movie data.

### Step-by-step TMDB key setup
1. Go to [TMDB API settings](https://www.themoviedb.org/settings/api)
2. Create an account or sign in
3. Request an API key (Developer option)
4. Copy your key
5. In this project, run:

```bash
python setup_api_key.py
```

6. Paste your key when asked
7. Choose where to save it:
   - `.env` (recommended)
   - `config.py`
   - or both

The current host setup using `config.py` is still supported and preserved.

### Manual setup option (if you prefer)
- Copy `config.py.example` to `config.py`
- Replace `your_api_key_here` with your real TMDB API key

### Test that API setup worked
Run:

```bash
python recommender.py
```

If working, you should see:
- `Using live movie data (TMDB).`
- `Fetching movie recommendations...`

If it fails, the app should safely fall back to local data.

## Advanced Version: Try a More ML-Style Recommender

This is a separate follow-up script for students after the main workshop:
- File: `advanced_recommender.py`
- Goal: learn collaborative filtering ideas with a real dataset

### What students learn in this version
- How a recommender changes when we use real user ratings
- What a user-item matrix is
- How movie similarity can be computed with cosine similarity
- Why this feels more like ML than simple rule-based logic

### Dataset to download
Download **MovieLens Latest Small** from:
- [MovieLens Datasets](https://grouplens.org/datasets/movielens/latest/)

You need the **`ml-latest-small.zip`** file.

### Where to place the dataset
After unzipping, place the folder so this path exists:
- `data/ml-latest-small/`

At minimum, these files should be inside it:
- `data/ml-latest-small/movies.csv`
- `data/ml-latest-small/ratings.csv`

Optional:
- `data/ml-latest-small/tags.csv`

### Install command (advanced only)

```bash
pip install -r requirements-advanced.txt
```

### Run the advanced script

```bash
python advanced_recommender.py
```

The script will:
1. Load MovieLens data
2. Build a movie-to-movie similarity engine
3. Ask for a movie title you like
4. Return similar movies as recommendations

## Friendly Error Behavior (for students)

The app now handles common beginner issues with clear messages:
- Empty input vibe
- Missing API key
- API request failure
- Missing local movie file
- No matching recommendations

## Workshop Notes (Host)

- Teach the basic local version first (`python recommender.py` with no API key required)
- Introduce API mode only after students understand input, tags, and scoring
- If TMDB fails live, keep teaching: the app auto-falls back to local movie data
- Before class, test both modes once on your machine

## Quick Test Commands

Install:

```bash
pip install -r requirements.txt
```

Run basic mode:

```bash
python recommender.py
```

Install advanced dependencies (only if needed):

```bash
pip install -r requirements-advanced.txt
```

Run advanced ML-style recommender:

```bash
python advanced_recommender.py
```

Run API setup helper:

```bash
python setup_api_key.py
```

Run with optional debug details (host only):

```bash
# Windows PowerShell
$env:MOVIE_RECS_DEBUG="1"; python recommender.py

# Mac/Linux
MOVIE_RECS_DEBUG=1 python recommender.py
```
