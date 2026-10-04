"""
Movie Recommender Workshop

This script is the beginner path for the workshop. It demonstrates two ideas:
1) Local rule-based recommendation using mood/tag overlap.
2) Optional live-data enrichment using the TMDB API.

The recommendation score in this file is deterministic; it is not a trained
machine-learning model. See advanced_recommender.py for the collaborative-
filtering extension built from MovieLens ratings.
"""

import json
import os
from pathlib import Path

import requests


PROJECT_ROOT = Path(__file__).resolve().parent
MOVIES_PATH = PROJECT_ROOT / "data" / "movies.json"

# Optional debug mode for host troubleshooting.
# Set MOVIE_RECS_DEBUG=1 to see additional technical details.
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

# Beginner-friendly aliases. Tags with no TMDB genre mapping still work with
# the local sample dataset.
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

GENRE_ID_TO_ALIASES = {}
for mood_word, genre_id in MOOD_TO_GENRE.items():
    if genre_id is not None:
        GENRE_ID_TO_ALIASES.setdefault(genre_id, []).append(mood_word)


def debug_print(message):
    """Print a message only when debug mode is enabled."""
    if DEBUG_MODE:
        print(f"[DEBUG] {message}")


def load_tmdb_api_key():
    """Load a TMDB API key from the project .env file or process environment."""
    try:
        from dotenv import load_dotenv

        load_dotenv(PROJECT_ROOT / ".env")
    except Exception as error:
        debug_print(f"Could not load .env file: {error}")

    return os.getenv("TMDB_API_KEY", "").strip()


TMDB_API_KEY = load_tmdb_api_key()


def parse_user_tags(raw_text):
    """Turn comma-separated text into a clean set of lowercase tags."""
    return {tag.strip().lower() for tag in raw_text.split(",") if tag.strip()}


def get_user_mood_tags():
    """Ask for vibe words and require at least one non-empty tag."""
    print("Welcome to the Movie Recommender Workshop")
    print("Describe your movie vibe with one or more words.")
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
    """Convert supported user mood words to TMDB genre IDs."""
    genre_ids = []
    for tag in user_tags:
        genre_id = MOOD_TO_GENRE.get(tag)
        if genre_id is not None and genre_id not in genre_ids:
            genre_ids.append(genre_id)
    return genre_ids


def build_tmdb_request_params(user_tags):
    """Build the TMDB endpoint and query parameters for the supplied tags."""
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
    """Convert one TMDB result to the workshop's internal movie format."""
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
        "rating": tmdb_movie.get("vote_average", 0),
        "release_date": tmdb_movie.get("release_date", "Unknown"),
    }


def fetch_movies_from_tmdb(user_tags, max_results=20):
    """Fetch live movies from TMDB, returning None when live data is unavailable."""
    if not TMDB_API_KEY:
        return None

    print("Using live movie data (TMDB).")
    print("Fetching movie recommendations...")

    try:
        url, params = build_tmdb_request_params(user_tags)
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as error:
        print("Live movie data is unavailable right now.")
        debug_print(f"TMDB request error: {error}")
        return None

    try:
        data = response.json()
    except ValueError as error:
        print("TMDB returned an unexpected response, so local data will be used.")
        debug_print(f"TMDB JSON parse error: {error}")
        return None

    tmdb_movies = data.get("results", [])[:max_results]
    converted_movies = [convert_tmdb_movie(movie) for movie in tmdb_movies]
    converted_movies = [movie for movie in converted_movies if movie.get("title")]

    if not converted_movies:
        print("Live data returned no results, so local data will be used.")
        return None

    return converted_movies


def load_movies_from_local_file():
    """Load the workshop's canonical local movie JSON file."""
    if not MOVIES_PATH.exists():
        print("Local movie data file is missing.")
        print(f"Expected: {MOVIES_PATH}")
        return []

    try:
        with MOVIES_PATH.open("r", encoding="utf-8") as file:
            movies = json.load(file)
    except json.JSONDecodeError as error:
        print("Local movie data file has invalid JSON format.")
        debug_print(f"JSON decode error in {MOVIES_PATH}: {error}")
        return []
    except OSError as error:
        print("The local movie data file could not be read.")
        debug_print(f"File read error in {MOVIES_PATH}: {error}")
        return []

    if not isinstance(movies, list):
        print("Local movie data is in an unexpected format.")
        return []

    return movies


def load_movies(user_tags, use_api=True):
    """Try live data first when configured, then fall back to local sample data."""
    if use_api and TMDB_API_KEY:
        movies = fetch_movies_from_tmdb(user_tags, max_results=20)
        if movies:
            return movies
        print("Switching to local movie data.")
    elif use_api:
        print("No API key found, so the local workshop dataset will be used.")

    print("Using local movie data.")
    return load_movies_from_local_file()


def score_movie(movie, user_tags):
    """Score one movie using deterministic tag overlap plus small bonuses."""
    movie_tags = {tag.lower() for tag in movie.get("mood_tags", [])}
    overlap = movie_tags & user_tags
    score = len(overlap)

    movie_genre = movie.get("genre", "").lower()
    if movie_genre in user_tags:
        score += 1

    if movie.get("rating", 0) >= 7.5:
        score += 0.5

    return score


def recommend_movies(movies, user_tags, top_k=5):
    """Score all movies and return the strongest positive matches."""
    scored_movies = [(score_movie(movie, user_tags), movie) for movie in movies]
    scored_movies.sort(key=lambda item: item[0], reverse=True)
    return [item for item in scored_movies if item[0] > 0][:top_k]


def collect_available_tags(movies):
    """Build a sorted list of tags users can try next."""
    all_tags = set()
    for movie in movies:
        for tag in movie.get("mood_tags", []):
            all_tags.add(tag.lower())
    return sorted(all_tags)


def print_recommendations(recommendations):
    """Display recommendations in a beginner-friendly format."""
    print()
    print("Your movie recommendations:")
    print()

    for rank, (score, movie) in enumerate(recommendations, start=1):
        print(f"{rank}. {movie.get('title', 'Untitled')} (match score: {score:.1f})")
        print(f"   Genre: {movie.get('genre', 'Unknown')}")

        mood_tags = movie.get("mood_tags", [])
        if mood_tags:
            print(f"   Mood tags: {', '.join(mood_tags[:5])}")

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
    """Run the beginner workshop recommender."""
    user_tags = get_user_mood_tags()
    movies = load_movies(user_tags, use_api=True)

    if not movies:
        print("No movie data is available right now.")
        return

    print(f"Loaded {len(movies)} movies.")
    recommendations = recommend_movies(movies, user_tags)

    if not recommendations:
        print("No strong matches found for that vibe yet.")
        print("Try entering one or two mood words like chill, funny, or action.")
        available_tags = collect_available_tags(movies)
        if available_tags:
            print(f"You can try tags like: {', '.join(available_tags[:12])}")
        return

    print_recommendations(recommendations)


if __name__ == "__main__":
    main()
