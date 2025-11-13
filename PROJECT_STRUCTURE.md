# Project Structure Guide — Understanding Your Movie Recommender

Welcome! This guide will help you understand how your Movie Night Recommender project is organized. You'll learn what each file does, how they work together, and how the program flows from start to finish.

## Table of Contents

1. [Root Level Files](#root-level-files)
2. [Code Files](#code-files)
3. [Data Files](#data-files)
4. [How Files Work Together](#how-files-work-together)
5. [Design Patterns](#design-patterns)
6. [File Dependencies](#file-dependencies)

---

## Root Level Files

### 1. README.md

**What it is**: The main documentation file for the project.

**What you'll find here**:
- Project overview and what you'll learn
- Features and capabilities of the program
- Setup instructions (how to install dependencies and configure API key)
- Usage examples (how the program works with and without API key)
- Supported mood tags and aliases
- Ideas for extending the project
- Troubleshooting guide (solutions to common problems)
- Useful links (TMDB API, Python libraries)

**Why it's useful**: This is usually the first file you read when exploring a project. It gives you a complete overview of what the project does and how to use it.

**Key sections you'll use**:
- What You'll Learn - Skills you'll gain from this project
- Setup - Step-by-step instructions to get started
- Run It - How to execute the program
- How It Works - Explanation of the recommendation process
- Example Usage - See what the output looks like
- Troubleshooting - Solutions if something goes wrong

---

### 2. START_HERE.md

**What it is**: A quick-start guide to get you running the program right away.

**What you'll find here**:
- Step-by-step instructions to run the program
- How to open terminal/command prompt
- How to navigate to your project folder
- How to install dependencies
- How to set up your API key
- How to run the program
- What to expect when the program runs
- Troubleshooting tips for common issues

**Why it's useful**: If you want to start coding immediately without reading all the documentation, this guide gets you up and running quickly.

**Key sections**:
- Quick Start Guide - Step-by-step instructions
- Troubleshooting - Solutions to common problems
- What to Expect - See what happens when you run the program
- Next Steps - Ideas for experimenting with the code
- Quick Commands Reference - Handy commands to remember

**How it's different from README.md**: 
- README.md has comprehensive documentation about the project
- START_HERE.md is a focused guide to get you started quickly

---

### 3. requirements.txt

**Purpose**: Lists all Python package dependencies required for the project.

**Contents**:
```
requests
python-dotenv
```

**Dependencies**:
- `requests`: Used for making HTTP API calls to TMDB API
- `python-dotenv`: Used for loading API keys from `.env` files (optional)

**Usage**: Users install dependencies with `pip install -r requirements.txt`

**Role**: Ensures all required packages are installed for the project to work.

---

### 4. .gitignore

**Purpose**: Specifies which files and directories should be ignored by Git version control.

**What it ignores**:
- `__pycache__/` - Compiled Python bytecode files
- `*.py[cod]` - Python compiled files
- `.env` - Environment variables file (contains API keys)
- `config.py` - User's API key configuration (contains sensitive data)
- IDE files (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`, `Thumbs.db`)
- Virtual environments (`env/`, `venv/`)
- Distribution files (`dist/`, `build/`)

**Role**: Prevents sensitive files (API keys) and unnecessary files from being committed to Git.

**Security**: Ensures API keys are never committed to version control.

---

### 5. config.py (You Create This File)

**What it is**: A file where you store your TMDB API key.

**What it contains**:
```python
TMDB_API_KEY = "your_api_key_here"
```

**How to create it**:
1. Copy `config.py.example` to `config.py`
2. Replace `"your_api_key_here"` with your actual API key
3. OR run `python setup_api_key.py` and it will create it for you automatically

**How the program uses it**:
- When you run `starter/recommender.py` or `solution/recommender.py`, the program reads this file
- It loads your API key so it can make requests to TMDB API
- The API key is used to authenticate your requests

**Important security note**:
- This file is in `.gitignore` (Git will not track it)
- It contains your API key, which is like a password
- Never share this file publicly or commit it to GitHub
- Keep it on your computer only

**Alternative**: You can also use a `.env` file instead (the `python-dotenv` library will load it)

---

### 6. config.py.example

**Purpose**: Template file that shows users how to configure their API key.

**Contents**:
```python
# TMDB API Configuration
# Get your free API key from: https://www.themoviedb.org/settings/api
#
# Instructions:
# 1. Copy this file to config.py: cp config.py.example config.py
# 2. Replace 'your_api_key_here' with your actual TMDB API key
# 3. The config.py file is in .gitignore, so your API key won't be committed to git

TMDB_API_KEY = "your_api_key_here"
```

**Role**: 
- Safe to commit to Git (contains no real API keys)
- Shows users the expected format
- Provides setup instructions
- Template for users to create their own `config.py`

**Usage**: Users copy this file to `config.py` and add their API key.

---

### 7. setup_api_key.py

**What it is**: A helper script that guides you through setting up your TMDB API key.

**What it does**:
This script makes it easy to get and configure your API key. It:
- Opens the TMDB API key page in your browser
- Guides you through getting your free API key
- Helps you save your API key to `.env` or `config.py`
- Handles errors gracefully

**How to use it**:
1. Run: `python setup_api_key.py`
2. The script will open TMDB's website in your browser
3. Follow the instructions to get your API key
4. Paste your API key when prompted
5. Choose where to save it (`.env` or `config.py`)
6. You're done! Now you can run the main program with API access

**Why it's helpful**:
- Makes setup easy and automated
- Opens the website for you
- Guides you through each step
- Handles errors if something goes wrong
- Gives you options for where to save your key

**What functions it contains**:
- `print_welcome()` - Shows welcome message
- `open_api_key_url()` - Opens TMDB website in your browser
- `get_api_key_from_user()` - Asks you to paste your API key
- `save_api_key_to_env()` - Saves API key to `.env` file
- `save_api_key_to_config()` - Saves API key to `config.py` file
- `main()` - Runs the entire setup process

---

## Code Files

### 8. starter/recommender.py

**What it is**: The main file you'll work with. It contains starter code with TODOs for you to complete.

**What you'll do here**:
This is where you'll write most of your code. The file has TODO comments marking sections you need to complete. This helps you learn Python concepts by implementing them yourself.

**File structure**:

#### **Configuration Section**

**API Key Loading**:
The program tries multiple ways to find your API key:
1. First, it checks environment variables
2. Then, it looks for a `.env` file
3. Finally, it tries to load from `config.py` file
4. If no API key is found, it uses an empty string (program will use local file)

**Constants**:
- `TMDB_BASE_URL`: The base URL for TMDB API (`https://api.themoviedb.org/3`)
- `MOVIES_PATH`: The path to your local `data/movies.json` file (used as fallback)

**Mappings**:
- `MOOD_TO_GENRE`: A dictionary that maps your mood tags to TMDB genre IDs
  - Example: When you type "funny", it maps to genre ID 35 (Comedy)
  - Example: When you type "action", it maps to genre ID 28 (Action)
  - Some tags like "chill" don't map to genres but are still used for matching

- `GENRE_ID_TO_ALIASES`: A reverse mapping that helps match aliases
  - Example: Genre 35 (Comedy) has aliases ["comedy", "funny"]
  - This means when a movie is tagged as "comedy", it also gets the "funny" tag
  - This helps "funny" user input match "comedy" movies

#### **Core Functions**:

**1. `fetch_movies_from_tmdb(user_tags, max_results=20)`**
- **Purpose**: Fetches movies from TMDB API based on user mood tags
- **Process**:
  1. Maps user tags to TMDB genre IDs using `MOOD_TO_GENRE`
  2. Filters out tags that don't map to genres (`None` values)
  3. If no genres matched, fetches popular movies
  4. If genres matched, fetches movies by genre using `/discover/movie` endpoint
  5. Makes HTTP GET request to TMDB API with API key
  6. Parses JSON response
  7. Converts TMDB format to internal format
  8. Adds aliases to movie tags (e.g., "comedy" movies get "funny" tag)
  9. Adds additional tags based on movie data (highly-rated, family-friendly, popular)
  10. Returns list of movies or `None` if API fails

- **Error Handling**:
  - Handles missing API key
  - Handles network errors
  - Handles API errors (status codes)
  - Handles JSON parsing errors
  - Returns `None` on failure (triggers fallback)

- **Returns**: List of movie dictionaries or `None`

**2. `load_movies_from_file()`**
- **Purpose**: Loads movies from local JSON file (fallback)
- **Process**:
  1. Opens `data/movies.json` file
  2. Reads JSON content
  3. Parses JSON to Python list of dictionaries
  4. Returns list of movies

- **Error Handling**:
  - Handles file not found errors
  - Handles JSON parsing errors
  - Returns empty list on error

- **Returns**: List of movie dictionaries

**3. `load_movies(user_tags, use_api=True)`**
- **Purpose**: Loads movies from API or local file (with fallback)
- **Process**:
  1. Checks if API key exists
  2. If API key exists and `use_api=True`, tries to fetch from TMDB API
  3. If API fails or no API key, falls back to local file
  4. Returns list of movies

- **Fallback Logic**:
  - API first (if key exists)
  - Local file if API fails
  - Local file if no API key
  - Always returns a list of movies (never fails completely)

- **Returns**: List of movie dictionaries

**4. `get_user_mood_tags()`**
- **Purpose**: Gets user's movie mood tags from command line input
- **Process**:
  1. Prints welcome message
  2. Shows API status (using API or local file)
  3. Prompts user for mood tags (comma-separated)
  4. Splits input by commas
  5. Strips whitespace from each tag
  6. Converts to lowercase
  7. Filters out empty strings
  8. Converts to set (removes duplicates)
  9. Returns set of mood tags

- **Example Input**: `"chill, funny, horror"`
- **Example Output**: `{"chill", "funny", "horror"}`

- **Returns**: Set of lowercase mood tag strings

**5. `score_movie(movie, user_tags)`**
- **Purpose**: Calculates a relevance score for a movie based on user mood tags
- **Scoring Algorithm**:
  1. Converts movie's mood tags to lowercase set
  2. Finds overlapping tags between movie and user (set intersection)
  3. Base score = number of matching tags (1 point per match)
  4. Genre bonus: +1 point if movie's genre matches user tag
  5. Rating bonus: +0.5 points if movie rating ≥ 7.5
  6. Returns total score

- **Example**:
  - Movie tags: `["comedy", "funny", "family-friendly"]`
  - User tags: `{"funny", "chill"}`
  - Overlap: `{"funny"}` (1 match)
  - Genre match: No (genre is "Comedy", not in user tags)
  - Rating bonus: Yes (rating 8.0 ≥ 7.5)
  - Score: 1 + 0.5 = 1.5

- **Returns**: Float score (higher = better match)

**6. `recommend_movies(movies, user_tags, top_k=5)`**
- **Purpose**: Scores all movies and returns top recommendations
- **Process**:
  1. Creates empty list for scored movies
  2. Loops through each movie
  3. Calculates score for each movie using `score_movie()`
  4. Stores (score, movie) tuples in list
  5. Sorts list by score (highest first)
  6. Filters out movies with score 0 (no matches)
  7. Returns top_k recommendations

- **Returns**: List of tuples `[(score, movie), ...]` sorted by score (highest first)

**7. `main()`**
- **Purpose**: Main entry point that orchestrates the entire program
- **Execution Flow**:
  1. Prints debug info (API key status)
  2. Gets user mood tags (`get_user_mood_tags()`)
  3. Loads movies (`load_movies()`)
  4. Calculates recommendations (`recommend_movies()`)
  5. Shows API demo info (`demo_real_api_pattern()`)
  6. Displays recommendations (formatted output)
  7. Handles empty recommendations gracefully

- **Error Handling**:
  - Handles no movies found
  - Handles no recommendations found
  - Provides helpful error messages

#### **Execution Flow**:

```
main()
  ↓
get_user_mood_tags()
  ↓ (returns user_tags)
load_movies(user_tags)
  ↓
  ├─→ fetch_movies_from_tmdb() [if API key exists]
  │     ↓
  │     └─→ TMDB API request
  │           ↓
  │           └─→ Convert to internal format
  │                 ↓
  │                 └─→ Add aliases to tags
  │
  └─→ load_movies_from_file() [if API fails or no key]
        ↓
        └─→ Read data/movies.json
  ↓ (returns movies list)
recommend_movies(movies, user_tags)
  ↓
  ├─→ score_movie() [for each movie]
  │     ↓
  │     └─→ Calculate score
  │
  └─→ Sort by score
        ↓
        └─→ Filter zero scores
          ↓
          └─→ Return top_k
  ↓ (returns recommendations)
Display results
```

#### **Key Features**:
- TODOs for you to complete (marked with "Student Task" comments)
- Extensive comments explaining Python concepts
- SCALE-UP comments showing how you could extend the code
- Error handling and fallbacks
- Debug output for troubleshooting
- Educational value (helps you learn Python basics)

---

### 9. solution/recommender.py

**What it is**: The complete, working solution with all code filled in.

**What you'll find here**:
- All TODOs completed
- Fully functional code
- More detailed comments explaining the concepts
- Additional error handling examples
- Same functionality as starter, fully implemented

**Key Differences from Starter**:
- No TODOs (all code is complete)
- More comprehensive comments explaining concepts
- Additional error handling examples
- More robust implementation
- Same API and functionality

**How you can use it**:
- Reference to check your work
- See how the complete solution looks
- Learn from the complete implementation
- Test and validate your understanding
- Compare your solution with the reference

**Why it's useful**: This gives you a complete reference so you can see how the finished code looks and compare it with your own implementation.

---

## Data Files

### 10. data/movies.json

**Purpose**: Local movie data file used as fallback when API is unavailable or not configured.

**Structure**:
```json
[
  {
    "id": 1,
    "title": "Black Panther",
    "genre": "Action",
    "mood_tags": ["action", "epic", "inspiring", "superhero", "adventure"],
    "description": "A powerful superhero film that celebrates African culture...",
    "platform": "Disney+"
  },
  ...
]
```

**Contents**: 8 movies with diverse genres:
1. Black Panther (Action)
2. The Lovebirds (Comedy)
3. Get Out (Horror)
4. Soul (Animation)
5. Queen & Slim (Drama)
6. Spy (Action)
7. Encanto (Animation)
8. Spiderman: Into the Spider-Verse (Action)

**Each Movie Contains**:
- `id`: Unique identifier
- `title`: Movie title
- `genre`: Primary genre
- `mood_tags`: List of mood tags for matching
- `description`: Movie description
- `platform`: Streaming platform (where to watch)

**When It's Used**:
- No API key configured
- API request fails (network error, API error)
- Offline usage (no internet)
- Testing without API
- Learning how the code works

**Role**: Ensures the program always works, even without API access.

**Benefits**:
- Always available (no internet required)
- Fast (no API calls)
- Consistent (same data every time)
- Good for testing and learning

---

## How Files Work Together

### Data Flow

```
User Input
  ↓
setup_api_key.py → config.py (or .env)
  ↓
starter/recommender.py
  ↓
  ├─→ Load API key from config.py or .env
  │
  ├─→ Get user mood tags (input)
  │
  ├─→ Load movies:
  │     ├─→ Try TMDB API (if key exists)
  │     │     └─→ fetch_movies_from_tmdb()
  │     │           └─→ Convert TMDB format to internal format
  │     │                 └─→ Add aliases to tags
  │     │
  │     └─→ Fallback to data/movies.json
  │           └─→ load_movies_from_file()
  │
  ├─→ Score movies:
  │     └─→ score_movie() [for each movie]
  │           └─→ Calculate relevance score
  │
  ├─→ Recommend movies:
  │     └─→ recommend_movies()
  │           └─→ Sort by score, return top_k
  │
  └─→ Display results
```

### Execution Flow

1. **Setup Phase**:
   - User runs `setup_api_key.py`
   - Script opens TMDB API page in browser
   - User gets API key from TMDB
   - Script saves API key to `config.py` or `.env`

2. **Execution Phase**:
   - User runs `python starter/recommender.py`
   - Program loads API key from `config.py` or `.env`
   - Program prompts user for mood tags
   - Program loads movies (API or local file)
   - Program scores movies based on user tags
   - Program displays top recommendations

3. **Scoring Phase**:
   - Each movie is scored based on:
     - Matching mood tags (1 point per match)
     - Genre match (1 bonus point)
     - High rating (0.5 bonus points)
   - Movies are sorted by score (highest first)
   - Top 5 movies are displayed

### File Interactions

**setup_api_key.py ↔ config.py**:
- `setup_api_key.py` creates/writes to `config.py`
- `config.py` is read by `starter/recommender.py` and `solution/recommender.py`

**starter/recommender.py ↔ config.py**:
- `starter/recommender.py` imports API key from `config.py`
- Uses API key to make TMDB API requests

**starter/recommender.py ↔ data/movies.json**:
- `starter/recommender.py` reads `data/movies.json` as fallback
- Used when API is unavailable or fails

**starter/recommender.py ↔ TMDB API**:
- Makes HTTP GET requests to TMDB API
- Uses API key for authentication
- Receives movie data in JSON format

**README.md ↔ START_HERE.md**:
- `README.md` references `START_HERE.md` for quick start
- `START_HERE.md` references `README.md` for detailed documentation

---

## Design Patterns

### 1. Fallback Pattern

**Purpose**: Ensures the program always works, even when external services fail.

**Implementation**:
- Try API first (if API key exists)
- Fall back to local file if API fails
- Multiple API key sources (env, `.env`, `config.py`)

**Benefits**:
- Reliability (always works)
- Graceful degradation (works offline)
- User experience (no complete failures)

**Example**:
```python
if use_api and TMDB_API_KEY:
    movies = fetch_movies_from_tmdb(user_tags)
if not movies:
    movies = load_movies_from_file()  # Fallback
```

### 2. Configuration Pattern

**Purpose**: Centralizes configuration and provides multiple configuration methods.

**Implementation**:
- Environment variables
- `.env` file (python-dotenv)
- `config.py` file (Python module)
- Priority order: `config.py` > `.env` > environment variable

**Benefits**:
- Flexibility (multiple methods)
- Security (keys not in code)
- Convenience (easy to change)

**Example**:
```python
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")
try:
    from config import TMDB_API_KEY as CONFIG_API_KEY
    if CONFIG_API_KEY:
        TMDB_API_KEY = CONFIG_API_KEY
except ImportError:
    pass
```

### 3. Modular Design

**Purpose**: Separates concerns into distinct, reusable functions.

**Implementation**:
- Each function has a single responsibility
- Functions are independent and testable
- Clear separation of concerns (loading, scoring, recommending)

**Benefits**:
- Maintainability (easy to modify)
- Testability (easy to test individual functions)
- Reusability (functions can be reused)
- Readability (clear structure)

**Example**:
```python
def fetch_movies_from_tmdb():  # Data loading
def score_movie():  # Scoring logic
def recommend_movies():  # Recommendation logic
```

### 4. Error Handling

**Purpose**: Handles errors gracefully and provides helpful feedback.

**Implementation**:
- Try/except blocks for all external operations
- Graceful degradation (fallback to local file)
- User-friendly error messages
- Debug output for troubleshooting

**Benefits**:
- Reliability (handles errors)
- User experience (helpful messages)
- Debugging (debug output)

**Example**:
```python
try:
    movies = fetch_movies_from_tmdb(user_tags)
except requests.RequestException as e:
    print(f"Network error: {e}")
    movies = load_movies_from_file()  # Fallback
```

### 5. Educational Pattern

**Purpose**: Teaches Python concepts through code and comments.

**Implementation**:
- Extensive comments explaining concepts
- TODOs for students to complete
- SCALE-UP comments showing extensions
- Beginner-friendly code structure

**Benefits**:
- Learning (teaches Python)
- Understanding (clear explanations)
- Extension (shows how to scale)

**Example**:
```python
# TODO: find overlapping tags (set intersection)
# Sets have a special operation called "intersection" (the & operator)
# It finds all items that are in BOTH sets
# Example: {1, 2, 3} & {2, 3, 4} = {2, 3}
overlap = movie_tags & user_tags
```

---

## File Dependencies

### Dependency Graph

```
starter/recommender.py
  ├── config.py (optional - for API key)
  ├── .env (optional - for API key)
  ├── data/movies.json (fallback data)
  ├── requirements.txt (dependencies)
  │   ├── requests
  │   └── python-dotenv
  └── TMDB API (external - if API key exists)

solution/recommender.py
  ├── config.py (optional - for API key)
  ├── .env (optional - for API key)
  ├── data/movies.json (fallback data)
  ├── requirements.txt (dependencies)
  │   ├── requests
  │   └── python-dotenv
  └── TMDB API (external - if API key exists)

setup_api_key.py
  ├── config.py.example (template)
  ├── .env (created if needed)
  └── config.py (created if needed)

README.md
  └── START_HERE.md (references)

START_HERE.md
  └── README.md (references)
```

### Dependency Details

**starter/recommender.py**:
- **Required**: `data/movies.json` (for fallback)
- **Optional**: `config.py` or `.env` (for API key)
- **External**: TMDB API (if API key exists)
- **Python Packages**: `requests`, `python-dotenv` (from `requirements.txt`)

**solution/recommender.py**:
- **Required**: `data/movies.json` (for fallback)
- **Optional**: `config.py` or `.env` (for API key)
- **External**: TMDB API (if API key exists)
- **Python Packages**: `requests`, `python-dotenv` (from `requirements.txt`)

**setup_api_key.py**:
- **Required**: `config.py.example` (template)
- **Creates**: `config.py` or `.env` (user's API key)
- **External**: TMDB API website (opens in browser)

**README.md**:
- **References**: `START_HERE.md` (for quick start)
- **Standalone**: Can be read independently

**START_HERE.md**:
- **References**: `README.md` (for detailed documentation)
- **Standalone**: Can be read independently

### Installation Dependencies

1. **Python 3.6+** (required)
2. **requests** (from `requirements.txt`)
3. **python-dotenv** (from `requirements.txt`, optional)
4. **TMDB API Key** (optional, from `config.py` or `.env`)

### Runtime Dependencies

1. **data/movies.json** (required for fallback)
2. **config.py** or `.env` (optional, for API key)
3. **Internet connection** (optional, for API access)
4. **TMDB API** (optional, if API key exists)

---

## Summary

This project is designed as an educational project that teaches Python programming through building a movie recommendation system. The project structure supports:

- **Learning**: Starter code with TODOs for you to complete
- **Reference**: Solution code so you can check your work and see the complete implementation
- **Flexibility**: Multiple configuration methods (API key storage)
- **Reliability**: Fallback mechanisms (local file if API fails)
- **Security**: API keys are not committed to Git
- **Usability**: Setup script and comprehensive documentation

Each file has a specific purpose and role in the overall system, working together to provide a complete, functional movie recommendation system that can work with or without API access.

---

## Additional Resources

- **TMDB API Documentation**: https://developer.themoviedb.org/docs
- **Python requests Library**: https://requests.readthedocs.io/
- **python-dotenv Library**: https://pypi.org/project/python-dotenv/
- **Project README**: See `README.md` for more information
- **Quick Start Guide**: See `START_HERE.md` for step-by-step instructions

