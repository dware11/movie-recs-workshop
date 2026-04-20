"""
Beginner-friendly AI Movie Recommender.

This script can run in two modes:
1) Basic mode: uses local movie data from JSON (safest for workshops)
2) Live API mode: uses TMDB for fresh movie results (optional extension)
"""

import json
import os
import sys
from pathlib import Path

import requests


# Recommender systems suggest items based on what a user seems to like.
# In this workshop, we use "vibe matching": if your mood words overlap with
# a movie's mood tags, that movie gets a higher score.

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Optional debug mode for host troubleshooting.
# Set MOVIE_RECS_DEBUG=1 in your terminal to see extra technical details.
DEBUG_MODE = os.getenv("MOVIE_RECS_DEBUG", "").strip() == "1"

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_GENRE_NAMES = {
    12: "Adventure",
    14: "Fantasy",
    16: "Animation",
    18: "Drama",
    27: "Horror",
    28: "Action",
    35: "Comedy",
    37: "Western",
    53: "Thriller",
    80: "Crime",
    99: "Documentary",
    878: "Science Fiction",
    9648: "Mystery",
    10402: "Music",
    10749: "Romance",
    10751: "Family",
    10752: "War",
    10770: "TV Movie",
}

# Support both the current root path and the old data/ path.
MOVIES_PATH_CANDIDATES = [
    PROJECT_ROOT / "movies.json",
    PROJECT_ROOT / "data" / "movies.json",
]

# Map beginner-friendly mood words to TMDB genre IDs.
# Some words (like "chill") do not map to a TMDB genre, but are still used
# when matching local movie tags.
MOOD_TO_GENRE = {
    "action": 28,
    "adventure": 12,
    "animation": 16,
    "animated": 16,
    "black-led": None,
    "chill": None,
    "comedy": 35,
    "cozy": None,
    "drama": 18,
    "emotional": None,
    "epic": None,
    "family": 10751,
    "fantasy": 14,
    "feel-good": None,
    "funny": 35,
    "horror": 27,
    "inspiring": None,
    "intense": None,
    "music": 10402,
    "musical": 10402,
    "rom-com": 10749,
    "romantic": 10749,
    "romcom": 10749,
    "sci-fi": 878,
    "scifi": 878,
    "superhero": 28,
    "thought-provoking": None,
    "thriller": 53,
}

# Reverse lookup so aliases like "funny" also match comedy movies from TMDB.
GENRE_ID_TO_ALIASES = {}
for mood_word, genre_id in MOOD_TO_GENRE.items():
    if genre_id is not None:
        GENRE_ID_TO_ALIASES.setdefault(genre_id, []).append(mood_word)


def debug_print(message):
    """Print only when debug mode is on."""
    if DEBUG_MODE:
        print(f"[DEBUG] {message}")


def load_tmdb_api_key():
    """Load API key from .env / environment, then allow config.py override."""
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except Exception as error:
        debug_print(f"Could not load .env file: {error}")

    api_key = os.getenv("TMDB_API_KEY", "").strip()

    # Keep compatibility with host setup that uses config.py.
    try:
        from config import TMDB_API_KEY as CONFIG_API_KEY

        if CONFIG_API_KEY and CONFIG_API_KEY.strip():
            api_key = CONFIG_API_KEY.strip()
            debug_print("Loaded API key from config.py")
    except Exception as error:
        debug_print(f"Could not load API key from config.py: {error}")

    return api_key


TMDB_API_KEY = load_tmdb_api_key()


def parse_user_tags(raw_text):
    """Turn comma-separated text into a clean set of lower-case tags."""
    return {tag.strip().lower() for tag in raw_text.split(",") if tag.strip()}


def get_user_mood_tags():
    """Ask for vibe words and make sure input is not empty."""
    print("Welcome to the AI Movie Recommender")
    print("Tell us your movie vibe with one or more words.")
    print("Examples: chill, funny, action")
    print()

    while True:
        raw_text = input("Describe your vibe (comma-separated): ").strip()
        mood_tags = parse_user_tags(raw_text)

        if mood_tags:
            print(f"Got it. Your vibe tags: {', '.join(sorted(mood_tags))}")
            return mood_tags

        print("Try entering one or two mood words like chill, funny, or action.")
        print()


def get_genre_ids_from_tags(user_tags):
    """Convert user mood words to TMDB genre IDs."""
    genre_ids = []
    for tag in user_tags:
        genre_id = MOOD_TO_GENRE.get(tag)
        if genre_id is not None and genre_id not in genre_ids:
            genre_ids.append(genre_id)
    return genre_ids


def build_tmdb_request_params(user_tags):
    """Build URL + query params for TMDB based on user tags."""
    genre_ids = get_genre_ids_from_tags(user_tags)
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "page": 1,
    }

    if genre_ids:
        params["sort_by"] = "popularity.desc"
        params["with_genres"] = ",".join(str(genre_id) for genre_id in genre_ids)
        return f"{TMDB_BASE_URL}/discover/movie", params

    return f"{TMDB_BASE_URL}/movie/popular", params


def convert_tmdb_movie(tmdb_movie):
    """Convert one TMDB movie result to the local workshop movie format."""
    genre_ids = tmdb_movie.get("genre_ids", [])
    genre_names = [TMDB_GENRE_NAMES.get(genre_id, "Unknown") for genre_id in genre_ids]

    mood_tags = []
    for genre_id in genre_ids:
        genre_name = TMDB_GENRE_NAMES.get(genre_id, "Unknown").lower()
        mood_tags.append(genre_name)
        mood_tags.extend(GENRE_ID_TO_ALIASES.get(genre_id, []))

    if tmdb_movie.get("vote_average", 0) >= 7.5:
        mood_tags.append("highly-rated")
    if tmdb_movie.get("adult") is False:
        mood_tags.append("family-friendly")
    if tmdb_movie.get("popularity", 0) > 100:
        mood_tags.append("popular")

    return {
        "id": tmdb_movie.get("id"),
        "title": tmdb_movie.get("title", "Untitled"),
        "genre": genre_names[0] if genre_names else "Unknown",
        "mood_tags": sorted(set(mood_tags)),
        "description": tmdb_movie.get("overview", "No description available."),
        "platform": "Various",
        "rating": tmdb_movie.get("vote_average", 0),
        "release_date": tmdb_movie.get("release_date", "Unknown"),
    }


def fetch_movies_from_tmdb(user_tags, max_results=20):
    """Try to fetch live movies from TMDB. Returns list or None on failure."""
    if not TMDB_API_KEY:
        return None

    print("Using live movie data (TMDB).")
    print("Fetching movie recommendations...")

    try:
        url, params = build_tmdb_request_params(user_tags)
        response = requests.get(url, params=params, timeout=10)
    except requests.RequestException as error:
        print("We couldn't fetch live movie data right now.")
        debug_print(f"TMDB request error: {error}")
        return None

    if response.status_code != 200:
        print("We couldn't fetch live movie data right now.")
        debug_print(f"TMDB status code: {response.status_code}")
        debug_print(f"TMDB response: {response.text[:200]}")
        return None

    try:
        data = response.json()
    except ValueError as error:
        print("TMDB returned an unexpected response, so we'll use local data.")
        debug_print(f"TMDB JSON parse error: {error}")
        return None

    tmdb_movies = data.get("results", [])[:max_results]
    converted_movies = [convert_tmdb_movie(movie) for movie in tmdb_movies]
    converted_movies = [movie for movie in converted_movies if movie.get("title")]

    if not converted_movies:
        print("Live data returned no results, so we'll use local data.")
        return None

    return converted_movies


def find_local_movies_file():
    """Find the first available local movies file path."""
    for path in MOVIES_PATH_CANDIDATES:
        if path.exists():
            return path
    return None


def load_movies_from_local_file():
    """Load local movies JSON for the beginner-safe workshop path."""
    movies_file = find_local_movies_file()
    if not movies_file:
        expected_paths = ", ".join(str(path) for path in MOVIES_PATH_CANDIDATES)
        print("Local movie data file is missing.")
        print("Please make sure movies.json exists in the project.")
        debug_print(f"Checked paths: {expected_paths}")
        return []

    try:
        with open(movies_file, "r", encoding="utf-8") as file:
            movies = json.load(file)
            if not isinstance(movies, list):
                print("Local movie data is in an unexpected format.")
                return []
            return movies
    except json.JSONDecodeError as error:
        print("Local movie data file has invalid JSON format.")
        debug_print(f"JSON decode error in {movies_file}: {error}")
        return []
    except OSError as error:
        print("We couldn't read the local movie data file.")
        debug_print(f"File read error in {movies_file}: {error}")
        return []


def load_movies(user_tags, use_api=True):
    """
    Load movies from API first (if possible), then fallback to local data.
    """
    if use_api and TMDB_API_KEY:
        movies = fetch_movies_from_tmdb(user_tags, max_results=20)
        if movies:
            return movies
        print("Switching to local movie data.")
    elif use_api and not TMDB_API_KEY:
        print("No API key found, so we'll use the basic version instead.")

    print("Using local movie data.")
    return load_movies_from_local_file()


def score_movie(movie, user_tags):
    """
    Score one movie based on vibe overlap.

    The more overlap between movie tags and user tags, the higher the score.
    """
    movie_tags = {tag.lower() for tag in movie.get("mood_tags", [])}
    overlap = movie_tags & user_tags
    score = len(overlap)

    # Small bonus if the main genre is one of the user's tags.
    movie_genre = movie.get("genre", "").lower()
    if movie_genre in user_tags:
        score += 1

    # Small bonus for highly-rated movies from TMDB.
    if movie.get("rating", 0) >= 7.5:
        score += 0.5

    return score


def recommend_movies(movies, user_tags, top_k=5):
    """Score all movies and return the top matches."""
    scored_movies = []
    for movie in movies:
        score = score_movie(movie, user_tags)
        scored_movies.append((score, movie))

    scored_movies.sort(key=lambda item: item[0], reverse=True)
    positive_matches = [item for item in scored_movies if item[0] > 0]
    return positive_matches[:top_k]


def collect_available_tags(movies):
    """Build a simple list of tags students can try next."""
    all_tags = set()
    for movie in movies:
        for tag in movie.get("mood_tags", []):
            all_tags.add(tag.lower())
    return sorted(all_tags)


def print_recommendations(recommendations):
    """Display recommendations in a clean beginner-friendly format."""
    print()
    print("Your movie recommendations:")
    print()

    for rank, (score, movie) in enumerate(recommendations, start=1):
        print(f"{rank}. {movie.get('title', 'Untitled')} (match score: {score:.1f})")
        print(f"   Genre: {movie.get('genre', 'Unknown')}")

        mood_tags = movie.get("mood_tags", [])
        if mood_tags:
            print(f"   Mood tags: {', '.join(mood_tags[:5])}")

        print(f"   Platform: {movie.get('platform', 'Unknown')}")

        if movie.get("rating"):
            print(f"   Rating: {movie['rating']:.1f}/10")

        release_date = movie.get("release_date", "")
        if release_date and release_date != "Unknown":
            print(f"   Release date: {release_date}")

        description = movie.get("description", "")
        if len(description) > 150:
            description = f"{description[:150]}..."
        if description:
            print(f"   Description: {description}")

        print()


def main():
    """Run the workshop recommender app."""
    user_tags = get_user_mood_tags()
    movies = load_movies(user_tags, use_api=True)

    if not movies:
        print("No movie data is available right now.")
        print("For workshop safety, check that movies.json exists in this project.")
        return

    print(f"Loaded {len(movies)} movies.")
    recommendations = recommend_movies(movies, user_tags)

    if not recommendations:
        print("No strong matches found for that vibe yet.")
        print("Try entering one or two mood words like chill, funny, or action.")
        available_tags = collect_available_tags(movies)
        if available_tags:
            sample_tags = ", ".join(available_tags[:12])
            print(f"You can try tags like: {sample_tags}")
        return

    print_recommendations(recommendations)


if __name__ == "__main__":
    main()
