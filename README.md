# AI Movie Night Recommender — Python + API Project

Build your own movie recommendation system in Python! This beginner-friendly project teaches you how to create a simple "AI" movie recommender with **real TMDB API integration**. You'll learn Python fundamentals while building something fun and useful.

> **🚀 New to this project?** See [START_HERE.md](START_HERE.md) for detailed step-by-step instructions to get started!

## What You'll Learn

- Python basics: variables, lists, dictionaries, sets, loops, functions
- Reading JSON data from a file (simulating an API)
- **Real API integration** with TMDB (The Movie Database)
- How APIs work (`requests.get()` demo)
- Ranking and sorting data to make recommendations
- Error handling and fallback mechanisms
- SCALE-UP concepts: How this could work with real APIs and user data

## Features

✨ **NEW: Real TMDB API Integration!**
- Fetches live movie data from TMDB API
- Falls back to local JSON file if API fails
- Maps user mood tags to movie genres
- Shows movie ratings and release dates
- Works with or without API key (uses local file as fallback)

## Quick Start (GitHub Users)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/movie-recs-workshop.git
   cd movie-recs-workshop
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key** (Optional but Recommended):
   ```bash
   python setup_api_key.py
   ```
   This script will guide you through getting your free TMDB API key.

4. **Run the program**:
   ```bash
   python starter/recommender.py
   ```

**Note**: The program works without an API key (uses local data), but getting a free API key from TMDB gives you access to live movie data!

## Setup

> **Note for GitHub Users**: If you cloned this repository, you'll need to get your own TMDB API key. The `config.py` file is not included in the repository (for security), but you can use `config.py.example` as a template or run `python setup_api_key.py` to set it up automatically.

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get TMDB API Key (Optional but Recommended)

**Important**: Each user needs to get their own free API key from TMDB. API keys are free and take just a few minutes to set up.

1. Go to https://www.themoviedb.org/ and create a free account
2. Go to Settings → API → Request API Key
3. Choose "Developer" option
4. Fill out the form (application name, website URL, etc.)
   - **Application URL**: You can use `http://localhost` or your GitHub repo URL
   - **Application Summary**: Brief description of your project (e.g., "Movie recommendation project" or "Learning Python API integration")
5. Copy your API key

### 3. Configure API Key

**Easy Way: Use the Setup Script (Recommended)**
```bash
python setup_api_key.py
```
This script will:
- Open the TMDB API key page in your browser
- Guide you through getting your API key
- Help you save it to `.env` or `config.py`

**Manual Way: Three Options**

**Option 1: Use .env file (Recommended)**
```bash
# Create a .env file in the project root
echo "TMDB_API_KEY=your_api_key_here" > .env
```

**Option 2: Use config.py**
```bash
# Copy the example file
cp config.py.example config.py
# Edit config.py and add your API key
```

**Option 3: Set Environment Variable**
```bash
# Windows (PowerShell)
$env:TMDB_API_KEY="your_api_key_here"

# Linux/Mac
export TMDB_API_KEY="your_api_key_here"
```

**Note:** If you don't set an API key, the program will use the local `data/movies.json` file as a fallback.

## Run It

```bash
# Start with the starter code (you'll complete the TODOs)
python starter/recommender.py

# Or check out the complete solution
python solution/recommender.py
```

## Project Structure

```
movie-recs-workshop/
├── README.md
├── requirements.txt
├── config.py.example     # Template for API key configuration
├── data/
│   └── movies.json       # Local movie data (fallback)
├── starter/
│   └── recommender.py    # Starter code with TODOs - complete these!
└── solution/
    └── recommender.py    # Complete reference solution (check your work)
```

## How It Works

1. **Get User Input**: Asks the user for their movie night "vibe" (e.g., "chill, funny, horror")
2. **Load Movies**: 
   - If API key is set: Fetches movies from TMDB API based on user's mood tags
   - If no API key or API fails: Uses local `data/movies.json` file
   - Movies from the API automatically include aliases (e.g., "comedy" movies also get "funny" tag)
3. **Score Movies**: Compares user's mood tags with each movie's tags (including aliases)
   - Each matching tag adds 1 point
   - Genre match adds 1 bonus point
   - Highly-rated movies (≥7.5) add 0.5 bonus points
4. **Recommend**: Returns the top matching movies sorted by score

## Example Usage

### With TMDB API Key

```
🎬 Welcome to the Movie Night Recommender!
✨ Using real TMDB API for live movie data!
Describe your vibe (comma-separated, e.g. chill, funny, horror): action, comedy

[TMDB] Fetching movies from API...
[TMDB] Successfully fetched 20 movies from API! 🎬
Loaded 20 movies.

🍿 Your Movie Night Recommendations:

1. Deadpool (score: 3.5)
   Genre: Action
   Mood tags: action, comedy, highly-rated, popular
   Platform: Various
   Rating: 8.0/10 ⭐
   Release Date: 2016-02-09
   Description: A fast-talking mercenary with a morbid sense of humor...
```

### Without API Key (Using Local File)

```
🎬 Welcome to the Movie Night Recommender!
💡 Tip: Get a free TMDB API key to use real movie data!
   Visit: https://www.themoviedb.org/settings/api
   Then set it in .env file or config.py
Describe your vibe (comma-separated, e.g. chill, funny, horror): chill, funny

[INFO] No TMDB API key found. Using local movies.json file.
Loaded 8 movies.

🍿 Your Movie Night Recommendations:

- The Lovebirds (score: 3.0)
  Genre: Comedy
  Mood tags: funny, romantic, chill, feel-good, rom-com
  Platform: Netflix
  Description: A hilarious rom-com about a couple who accidentally witness a murder...
```

## Supported Mood Tags

The program maps user mood tags to TMDB genres:

- **Genres**: action, adventure, comedy, drama, horror, romantic, sci-fi, thriller, animation, family, fantasy, musical
- **Mood Tags**: chill, cozy, feel-good, epic, inspiring, thought-provoking, emotional, intense, black-led
- **Aliases**: funny (comedy), rom-com (romantic), scifi (sci-fi), animated (animation), superhero (action), musical (music)

**Note**: The program automatically handles aliases, so entering "funny" will match "comedy" movies, "rom-com" will match "romantic" movies, etc. This ensures better matching between user input and movie recommendations.

## SCALE-UP Ideas

Once you've completed the basics, here are some ways you can extend this project:
- ✅ **Real API Integration** - Already implemented with TMDB!
- Call other movie APIs (OMDb) for additional movie data
- Pull user preferences from a user profile or database
- Use machine learning for smarter recommendations
- Filter by streaming platform availability
- Consider user watch history and ratings
- Add caching to reduce API calls and improve speed
- Implement pagination to show more results
- Add retry logic for handling failed API requests
- Create a web interface or mobile app
- Add user accounts to save preferences

## Requirements

- Python 3.6+
- requests library
- python-dotenv (optional, for .env file support)

Install with: `pip install -r requirements.txt`

## Troubleshooting

### API Key Not Working
- Make sure your API key is correct
- Check that you've set it in `.env`, `config.py`, or as an environment variable
- The program will fall back to local file if API fails

### No Movies Found
- Check your internet connection (if using API)
- Verify that `data/movies.json` exists (if using local file)
- Try different mood tags (e.g., "action", "comedy", "drama")

### API Rate Limiting
- TMDB has rate limits on free API keys
- If you hit rate limits, the program will fall back to local file
- Consider implementing caching for production use

### Low Scores (0.5 or below)
- Scores are based on matching tags between your input and movie tags
- A score of 0.5 usually means only the high-rating bonus matched (movie rated ≥7.5)
- **Solution**: Try using genre names directly (e.g., "comedy", "action", "drama")
- The program automatically handles aliases (e.g., "funny" matches "comedy" movies)
- If you see low scores, try broader or more common tags like "action", "comedy", "horror", "drama"

## Next Steps

After completing the starter code, try these enhancements:
- Add more mood tags to the mapping
- Improve the scoring algorithm for better recommendations
- Add more features (movie posters, trailers, reviews)
- Implement caching to speed up repeated searches
- Integrate with other movie APIs for more data
- Build a simple web interface
- Create a command-line interface with menus

## License

This project is for educational purposes.

## Useful Links

### TMDB API
- **Get API Key**: https://www.themoviedb.org/settings/api
- **Sign Up**: https://www.themoviedb.org/signup
- **API Documentation**: https://developer.themoviedb.org/docs
- **Genre List**: https://developer.themoviedb.org/reference/genre-movie-list
- **Discover Movies**: https://developer.themoviedb.org/reference/discover-movie
- **API Status**: https://status.themoviedb.org/

### Python Libraries
- **requests**: https://requests.readthedocs.io/
- **python-dotenv**: https://pypi.org/project/python-dotenv/
- **Pathlib**: https://docs.python.org/3/library/pathlib.html

### TMDB Genre IDs
- Action: 28, Adventure: 12, Animation: 16, Comedy: 35, Drama: 18
- Family: 10751, Fantasy: 14, Horror: 27, Music: 10402
- Romance: 10749, Science Fiction: 878, Thriller: 53

## Credits

- **TMDB API**: https://www.themoviedb.org/
- **Python requests**: https://requests.readthedocs.io/
