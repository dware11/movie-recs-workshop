"""
Movie Night Recommender — Complete Reference Solution

This is the complete, working solution with all code filled in.
Use this as a reference to check your work or see how the final solution looks.

What you'll learn from this sod processing text from the user
- API Basics: Making HTTP requests with the requests library
- Real API Integration: Using TMDB API for live movie data
- Error Handling: Handling API failures and fallbacks gracefully

Key Concepts Demonstrated:
- Reading and parsing JSON data
- Working with sets to find matching tags
- Sorting data by scores
- Making API calls and handling responses
- Converting data formats
- Error handling and fallback mechanismslution:
- File I/O: Reading JSON files
- Data Structures: Lists, dictionaries, sets, tuples
- Set Operations: Intersection (&), membership (in)
- List Comprehensions: Creating new lists from existing ones
- Functions: Breaking code into reusable pieces
- User Input: Getting an

SCALE-UP ideas: The code includes comments showing how you could extend this with
user profiles, machine learning, caching, and more advanced features.
"""

import json
from pathlib import Path
import requests
import os
import sys

# Add parent directory to Python path so we can import config.py
# This is needed because config.py is in the parent directory (project root)
# and solution/recommender.py is in the solution/ subdirectory
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Try to load environment variables from .env file (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except (ImportError, Exception):
    # If python-dotenv is not installed or .env file has issues, that's okay
    # We'll fall back to config.py or environment variables
    pass

# ---------- 0. Configuration ----------

# TMDB API Configuration
# Get your free API key from: https://www.themoviedb.org/settings/api
# Option 1: Set it as an environment variable: export TMDB_API_KEY="your_key_here"
# Option 2: Put it directly in config.py (see config.py.example)
# Option 3: Use .env file (see .env.example)
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")  # Will use "" if not set

# Try to load from config.py if it exists (alternative method)
# This takes priority over environment variables if .env fails
try:
    from config import TMDB_API_KEY as CONFIG_API_KEY
    if CONFIG_API_KEY:
        TMDB_API_KEY = CONFIG_API_KEY
        print(f"[DEBUG] Loaded API key from config.py: {TMDB_API_KEY[:10]}...")
except ImportError as e:
    config_path = project_root / "config.py"
    if config_path.exists():
        print(f"[DEBUG] config.py exists but import failed: {e}")
    else:
        print(f"[DEBUG] config.py not found at: {config_path}")
    pass  # config.py doesn't exist, that's okay
except Exception as e:
    print(f"[DEBUG] Error loading config.py: {e}")
    import traceback
    traceback.print_exc()
    pass

TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Path to local movies.json file (fallback if API fails)
MOVIES_PATH = Path(__file__).resolve().parent.parent / "data" / "movies.json"

# Map mood tags to TMDB genre IDs
# TMDB genre IDs: https://developer.themoviedb.org/reference/genre-movie-list
MOOD_TO_GENRE = {
    "action": 28,        # Action
    "adventure": 12,     # Adventure
    "comedy": 35,        # Comedy
    "funny": 35,         # Comedy (alias)
    "drama": 18,         # Drama
    "horror": 27,        # Horror
    "romantic": 10749,   # Romance
    "rom-com": 10749,    # Romance (alias)
    "romcom": 10749,     # Romance (alias)
    "sci-fi": 878,       # Science Fiction
    "scifi": 878,        # Science Fiction (alias)
    "thriller": 53,      # Thriller
    "animation": 16,     # Animation
    "animated": 16,      # Animation (alias)
    "family": 10751,     # Family
    "fantasy": 14,       # Fantasy
    "superhero": 28,     # Action (superhero movies are usually action)
    "musical": 10402,    # Music
    "music": 10402,      # Music (alias)
    "chill": None,       # These don't map to genres, but we'll use them for mood matching
    "cozy": None,        # These will be used for mood tag matching
    "feel-good": None,   # These will be used for mood tag matching
    "epic": None,        # These will be used for mood tag matching
    "inspiring": None,   # These will be used for mood tag matching
    "thought-provoking": None,  # These will be used for mood tag matching
    "emotional": None,   # These will be used for mood tag matching
    "intense": None,     # These will be used for mood tag matching
    "black-led": None,   # These will be used for mood tag matching
}

# Create reverse mapping: genre_id -> list of aliases
# This helps us add all aliases to movie tags so "funny" matches "comedy" movies
GENRE_ID_TO_ALIASES = {}
for alias, genre_id in MOOD_TO_GENRE.items():
    if genre_id is not None:
        if genre_id not in GENRE_ID_TO_ALIASES:
            GENRE_ID_TO_ALIASES[genre_id] = []
        GENRE_ID_TO_ALIASES[genre_id].append(alias.lower())

# ---------- 1. Configuration and Data Loading ----------

def fetch_movies_from_tmdb(user_tags, max_results=20):
    """
    Fetch movies from TMDB API based on user mood tags.
    
    This function:
    1. Maps user mood tags to TMDB genre IDs
    2. Fetches popular movies from TMDB for those genres
    3. Converts TMDB format to our format
    4. Returns a list of movies
    
    SCALE-UP: This is where we'd add:
    - Caching to avoid repeated API calls
    - Pagination to get more results
    - Filtering by release date, ratings, etc.
    - User-specific recommendations based on watch history
    - Filtering by streaming platform availability
    - Rate limiting to respect API limits
    - Retry logic for failed requests
    
    Args:
        user_tags: Set of user mood tags (e.g., {"action", "comedy"})
        max_results: Maximum number of movies to return
    
    Returns:
        List of movie dictionaries in our format, or None if API fails
    """
    if not TMDB_API_KEY:
        print("[INFO] No TMDB API key found. Using local movies.json file.")
        print("[INFO] Get a free API key from: https://www.themoviedb.org/settings/api")
        return None
    
    try:
        # Map user tags to TMDB genre IDs
        # Filter out None values (tags that don't map to genres)
        genre_ids = []
        for tag in user_tags:
            if tag in MOOD_TO_GENRE and MOOD_TO_GENRE[tag] is not None:
                genre_id = MOOD_TO_GENRE[tag]
                if genre_id not in genre_ids:
                    genre_ids.append(genre_id)
        
        # If no genres matched, use popular movies
        if not genre_ids:
            print("[INFO] No matching genres found. Fetching popular movies...")
            url = f"{TMDB_BASE_URL}/movie/popular"
            params = {
                "api_key": TMDB_API_KEY,
                "language": "en-US",
                "page": 1,
            }
        else:
            # Fetch movies by genre
            # Join genre IDs with commas for TMDB API
            genre_ids_str = ",".join(map(str, genre_ids))
            url = f"{TMDB_BASE_URL}/discover/movie"
            params = {
                "api_key": TMDB_API_KEY,
                "language": "en-US",
                "sort_by": "popularity.desc",  # Sort by popularity
                "with_genres": genre_ids_str,
                "page": 1,
            }
        
        print(f"[TMDB] Fetching movies from API...")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            tmdb_movies = data.get("results", [])[:max_results]
            
            # Convert TMDB format to our format
            movies = []
            
            # Map genre IDs to genre names
            genre_name_map = {
                28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
                80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
                14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
                9648: "Mystery", 10749: "Romance", 878: "Science Fiction",
                10770: "TV Movie", 53: "Thriller", 10752: "War", 37: "Western"
            }
            
            for tmdb_movie in tmdb_movies:
                # Get genre IDs from TMDB response
                genre_ids_from_api = tmdb_movie.get("genre_ids", [])
                
                # Map genre IDs to genre names
                genre_names = [genre_name_map.get(gid, "Unknown") for gid in genre_ids_from_api]
                
                # Create mood tags from genres and movie data
                mood_tags = []
                for genre_name in genre_names:
                    genre_lower = genre_name.lower()
                    mood_tags.append(genre_lower)
                    
                    # Add aliases for this genre so user tags like "funny" match "comedy" movies
                    # Find the genre ID for this genre name
                    genre_id = None
                    for gid, gname in genre_name_map.items():
                        if gname.lower() == genre_lower:
                            genre_id = gid
                            break
                    
                    # Add all aliases for this genre ID
                    if genre_id and genre_id in GENRE_ID_TO_ALIASES:
                        mood_tags.extend(GENRE_ID_TO_ALIASES[genre_id])
                
                # Add additional mood tags based on movie data
                if tmdb_movie.get("vote_average", 0) >= 7.5:
                    mood_tags.append("highly-rated")
                if tmdb_movie.get("adult") == False:
                    mood_tags.append("family-friendly")
                if tmdb_movie.get("popularity", 0) > 100:
                    mood_tags.append("popular")
                
                # Build our movie format
                movie = {
                    "id": tmdb_movie.get("id"),
                    "title": tmdb_movie.get("title"),
                    "genre": genre_names[0] if genre_names else "Unknown",
                    "mood_tags": list(set(mood_tags)),  # Remove duplicates
                    "description": tmdb_movie.get("overview", "No description available."),
                    "platform": "Various",  # TMDB doesn't provide streaming info in free tier
                    "rating": tmdb_movie.get("vote_average", 0),
                    "release_date": tmdb_movie.get("release_date", "Unknown"),
                }
                movies.append(movie)
            
            print(f"[TMDB] Successfully fetched {len(movies)} movies from API! 🎬")
            return movies
        else:
            print(f"[TMDB] API request failed with status: {response.status_code}")
            # Show error response for debugging
            try:
                error_data = response.json()
                if "status_message" in error_data:
                    print(f"[TMDB] Error message: {error_data['status_message']}")
                else:
                    print(f"[TMDB] Response: {response.text[:200]}")
            except:
                print(f"[TMDB] Response: {response.text[:200]}")
            return None
            
    except requests.RequestException as e:
        print(f"[TMDB] Network error fetching from API: {e}")
        print(f"[TMDB] Error type: {type(e).__name__}")
        return None
    except Exception as e:
        print(f"[TMDB] Unexpected error: {e}")
        print(f"[TMDB] Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return None

def load_movies_from_file():
    """
    Load movies from a local JSON file.
    
    This is used as a fallback if the API fails or if no API key is provided.
    
    SCALE-UP: In a real application, this data might come from:
    - A movie database API (TMDB, OMDb) to get hundreds of movies
    - A streaming platform API (Netflix, Hulu) for available content
    - A database with user ratings and reviews
    - A cloud storage service (S3, Firebase)
    - A recommendation service API
    
    Returns:
        list: A list of dictionaries, where each dictionary represents one movie
    """
    try:
        # Use 'with' statement to ensure file is properly closed after reading
        # 'r' mode means read-only
        # encoding="utf-8" handles special characters (emojis, accents, etc.)
        with open(MOVIES_PATH, "r", encoding="utf-8") as f:
            # json.load() parses the JSON file and converts it to Python objects:
            # - JSON arrays → Python lists
            # - JSON objects → Python dictionaries
            # - JSON strings → Python strings
            # - JSON numbers → Python int/float
            # - JSON booleans → Python bool
            movies = json.load(f)
        return movies
    except FileNotFoundError:
        print(f"[ERROR] Local movies file not found: {MOVIES_PATH}")
        return []
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in movies file: {e}")
        return []

def load_movies(user_tags, use_api=True):
    """
    Load movies from TMDB API or local file.
    
    This function tries to use the API first, then falls back to local file.
    
    SCALE-UP: This is where we'd add:
    - Caching API responses
    - Retry logic for failed API calls
    - Multiple API sources
    - Database integration
    
    Args:
        user_tags: Set of user mood tags
        use_api: Whether to try using the API first (default: True)
    
    Returns:
        List of movie dictionaries
    """
    movies = []
    
    # Debug: Check if API key is loaded
    if use_api:
        if TMDB_API_KEY:
            print(f"[DEBUG] API key is set: {TMDB_API_KEY[:10]}... (length: {len(TMDB_API_KEY)})")
        else:
            print("[DEBUG] No API key found - will use local file")
    
    if use_api and TMDB_API_KEY:
        # Try to fetch from TMDB API
        print(f"[DEBUG] Attempting to fetch movies from TMDB API...")
        movies = fetch_movies_from_tmdb(user_tags, max_results=20)
    
    # Fallback to local file if API failed or no API key
    if not movies:
        if TMDB_API_KEY:
            print("[INFO] API call failed or returned no results. Using local movies.json file...")
        else:
            print("[INFO] No API key configured. Using local movies.json file...")
        movies = load_movies_from_file()
    
    return movies

def demo_real_api_pattern():
    """
    Demonstrate how to make an API call using the requests library.
    This is now replaced by the actual TMDB integration above.
    """
    if TMDB_API_KEY:
        print("\n[API DEMO] ✅ We're using the real TMDB API for movie recommendations!")
        print("[API DEMO] This means you're getting live, up-to-date movie data! 🎬")
    else:
        print("\n[API DEMO] 💡 No API key configured. Using local data.")
        print("[API DEMO] To use real API: Get free API key from https://www.themoviedb.org/settings/api")

# ---------- 2. User Input Processing ----------

def get_user_mood_tags():
    """
    Get and process user mood tags from command line input.
    
    This function:
    1. Prompts the user to enter their movie night vibe
    2. Splits the input by commas
    3. Cleans each tag (removes whitespace, converts to lowercase)
    4. Filters out empty strings
    5. Returns a set of mood tags
    
    SCALE-UP: Instead of asking via input(), we could:
    - Look up the user's "favorite genres" from a database or API
    - Pull tags from their watch history (what they've watched before)
    - Use machine learning to predict preferences from past behavior
    - Get preferences from a user profile stored in the cloud
    - Allow users to save their favorite mood tags for quick access
    - Analyze social media to infer mood preferences
    - Consider time of day, weather, or calendar events
    
    Returns:
        set: A set of lowercase strings representing user mood tags
    
    Example:
        Input: "chill, funny, cozy"
        Output: {"chill", "funny", "cozy"}
    """
    # Print welcome message
    print("🎬 Welcome to the Movie Night Recommender!")
    
    if TMDB_API_KEY:
        print("✨ Using real TMDB API for live movie data!")
    else:
        print("💡 Tip: Get a free TMDB API key to use real movie data!")
        print("   Quick setup: Run 'python setup_api_key.py'")
        print("   Or visit: https://www.themoviedb.org/settings/api")
        print("   Then set it in .env file or config.py")
    
    # Get input from user
    # input() pauses execution and waits for user to type and press Enter
    # The string they type is returned and stored in 'raw'
    raw = input("Describe your vibe (comma-separated, e.g. chill, funny, horror): ")

    # Process the input string:
    # 1. raw.split(",") splits the string by commas
    #    Example: "chill, funny, cozy" → ["chill", " funny", " cozy"]
    #
    # 2. {tag.strip().lower() for tag in ...} is a set comprehension
    #    It creates a set by looping through each tag and processing it
    #
    # 3. tag.strip() removes leading/trailing whitespace
    #    Example: " funny" → "funny"
    #
    # 4. .lower() converts to lowercase for case-insensitive matching
    #    Example: "Funny" → "funny"
    #
    # 5. if tag.strip() filters out empty strings
    #    This handles cases like "chill,," or ",funny"
    #
    # 6. The curly braces {} create a set (not a list)
    #    Sets are faster for membership tests and intersections
    mood_tags = {tag.strip().lower() for tag in raw.split(",") if tag.strip()}

    # Show the user what we interpreted
    print("\nYou said your vibe is:", mood_tags)
    
    return mood_tags

# ---------- 3. Movie Scoring and Recommendation Logic ----------

def score_movie(movie, user_tags):
    """
    Calculate a relevance score for a movie based on user mood tags.
    
    Scoring rules:
    - Each matching mood tag adds 1 point
    - If the movie genre matches a user tag, add 1 bonus point
    - If the movie has a high rating (>= 7.5), add 0.5 bonus points
    
    SCALE-UP:
    - Add weights (e.g. "comfort" tags count more, "horror" tags count less for some users)
    - Add a "popularity" or rating field to boost highly-rated movies
    - Consider user's past ratings (collaborative filtering)
    - Use machine learning models to predict how much a user will like a movie
    - Factor in time of day, day of week (weekend vs weekday preferences)
    - Consider movie length (sometimes people want short movies)
    - Add diversity (don't recommend only one genre)
    - Factor in user's current mood detected from other signals
    - Consider social signals (what friends are watching)
    
    Args:
        movie: A dictionary representing a movie
               Must have keys: "mood_tags" (list), "genre" (string)
        user_tags: A set of strings (user's mood tags)
    
    Returns:
        int: A score indicating how well the movie matches user mood
             Higher score = better match
    
    Example:
        Movie: {"mood_tags": ["chill", "funny"], "genre": "Comedy"}
        User tags: {"chill", "funny"}
        Score: 3 (2 matching tags + 1 genre bonus)
    """
    # Convert movie mood tags to a set of lowercase strings
    # Sets are perfect for this because:
    # 1. They automatically remove duplicates
    # 2. Set operations (intersection, union) are very fast
    # 3. Membership tests are O(1) instead of O(n) for lists
    
    # movie.get("mood_tags", []) safely gets the "mood_tags" key
    # If "mood_tags" doesn't exist, it returns [] (empty list) instead of raising an error
    # This is defensive programming - handles missing data gracefully
    movie_tags = {t.lower() for t in movie.get("mood_tags", [])}

    # Find overlapping tags using set intersection
    # The & operator finds elements that are in BOTH sets
    # Example: {"chill", "funny"} & {"funny", "cozy"} = {"funny"}
    overlap = movie_tags & user_tags

    # Base score: number of matching tags
    # Each matching tag is worth 1 point
    score = len(overlap)

    # Bonus point: if the movie's genre matches one of the user's tags
    # This gives a small boost to movies that are in a genre the user likes
    # Example: If user likes "horror" and movie genre is "Horror", add 1 point
    genre = movie.get("genre", "").lower()
    if genre in user_tags:
        score += 1

    # Bonus: if movie has high rating (from TMDB), add a small boost
    if movie.get("rating", 0) >= 7.5:
        score += 0.5  # Small boost for highly-rated movies

    return score

def recommend_movies(movies, user_tags, top_k=5):
    """
    Score all movies and return the top recommendations.
    
    This function:
    1. Scores each movie using score_movie()
    2. Sorts movies by score (highest first)
    3. Filters out movies with score 0 (no matches)
    4. Returns the top_k movies
    
    SCALE-UP:
    - Add filtering by platform (user might only have Netflix)
    - Filter by availability (only show movies available now)
    - Add personalization based on user's watch history
    - Consider movie length preferences
    - Add diversity to avoid recommending only similar movies
    - Implement A/B testing to improve recommendations
    - Add re-ranking based on multiple factors (score, popularity, diversity)
    - Consider user's current subscription services
    - Filter by parental ratings if needed
    - Add "similar to" recommendations based on a selected movie
    
    Args:
        movies: A list of movie dictionaries
        user_tags: A set of strings (user's mood tags)
        top_k: Number of top recommendations to return (default: 5)
    
    Returns:
        list: A list of tuples [(score, movie), (score, movie), ...]
              Sorted by score (highest first), with zero-score movies removed
              Limited to top_k items
    
    Example:
        Input: 8 movies, user_tags={"chill", "funny"}, top_k=3
        Output: [(3, movie1), (2, movie2), (1, movie3)]
    """
    # List comprehension: create a list of (score, movie) tuples
    # This is more concise than the for loop version
    # For each movie, calculate its score and pair it with the movie
    scored = [(score_movie(movie, user_tags), movie) for movie in movies]
    
    # Sort the list by score (highest to lowest)
    # key=lambda p: p[0] means "sort by the first element of each tuple" (the score)
    # reverse=True means sort in descending order (highest scores first)
    scored.sort(key=lambda p: p[0], reverse=True)
    
    # Filter out movies with zero score (no matches)
    # List comprehension: keep only items where score > 0
    # item[0] is the score, item[1] is the movie
    scored = [item for item in scored if item[0] > 0]
    
    # Return only the top_k recommendations
    # [:top_k] is list slicing: takes first top_k items
    # Example: [1, 2, 3, 4, 5][:3] = [1, 2, 3]
    return scored[:top_k]

# ---------- 4. Main Program Execution ----------

def main():
    """
    Main function that orchestrates the entire recommendation process.
    
    This is the entry point of the program when run as a script.
    The flow is:
    1. Get user mood tags
    2. Load movies from API or local file
    3. Calculate recommendations
    4. Display results
    5. Show API demo
    """
    # Debug: Check API key status at startup
    print(f"[DEBUG] TMDB_API_KEY is set: {bool(TMDB_API_KEY)}")
    if TMDB_API_KEY:
        print(f"[DEBUG] API key length: {len(TMDB_API_KEY)} characters")
    
    # Step 1: Get user input FIRST (so we can use it to fetch from API)
    user_tags = get_user_mood_tags()

    # Step 2: Load movie data (from API or local file)
    movies = load_movies(user_tags, use_api=True)
    
    if not movies:
        print("❌ No movies found! Please check your API key or local file.")
        return
    
    print(f"Loaded {len(movies)} movies.")

    # Step 3: Calculate recommendations
    # Score all movies and get the top matches
    recommendations = recommend_movies(movies, user_tags)

    # Step 4: Show API demo (educational)
    # This demonstrates how real APIs work, but doesn't affect recommendations
    demo_real_api_pattern()

    # Step 5: Display results
    print("\n🍿 Your Movie Night Recommendations:\n")
    
    # Check if we found any recommendations
    if not recommendations:
        # If no matches found, give helpful feedback
        print("Hmm... no strong matches. Try different or broader vibes next time! 😅")
        # Show available tags to help user
        available_tags = set()
        for movie in movies:
            available_tags.update(tag.lower() for tag in movie.get("mood_tags", []))
        if available_tags:
            print(f"Available mood tags to try: {', '.join(sorted(available_tags)[:10])}")
        return  # Exit early if no recommendations

    # Loop through each recommendation and print details
    # 'enumerate' gives us both the index and the item
    # We use it to number the recommendations (1st, 2nd, 3rd, etc.)
    for rank, (score, movie) in enumerate(recommendations, start=1):
        # Print ranking and movie title with score
        # f-strings allow us to insert variables directly into strings
        print(f"{rank}. {movie['title']}  (score: {score:.1f})")
        
        # Print genre
        # movie.get('genre', 'unknown') safely gets genre or defaults to 'unknown'
        print(f"   Genre: {movie.get('genre', 'unknown')}")
        
        # Print mood tags as a comma-separated string
        # ', '.join() converts a list to a string with commas
        # Example: ['chill', 'funny'] → "chill, funny"
        tags_to_show = movie.get('mood_tags', [])[:5]  # Show first 5 tags
        tags_str = ', '.join(tags_to_show)
        print(f"   Mood tags: {tags_str}")
        
        # Print platform (where to watch)
        print(f"   Platform: {movie.get('platform', 'Unknown platform')}")
        
        # Print rating if available (from TMDB)
        if movie.get('rating'):
            print(f"   Rating: {movie['rating']:.1f}/10 ⭐")
        
        # Print release date if available
        if movie.get('release_date') and movie.get('release_date') != "Unknown":
            print(f"   Release Date: {movie['release_date']}")
        
        # Print description (truncate if too long)
        description = movie.get('description', '')
        if len(description) > 150:
            description = description[:150] + "..."
        print(f"   Description: {description}")
        
        # Print ID (useful for debugging or if implementing a "more info" feature)
        print(f"   ID: {movie.get('id', 'N/A')}\n")

# This is a Python idiom that means:
# "Only run main() if this script is executed directly"
# If someone imports this file as a module, main() won't run
# This allows the file to be both a runnable script AND an importable module
if __name__ == "__main__":
    main()
