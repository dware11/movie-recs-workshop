# 🚀 Start Here - How to Run the Movie Night Recommender

Welcome! This guide will help you get started with the Movie Night Recommender project. Follow these simple steps to run the program and start getting movie recommendations.

## Quick Start Guide

### Step 1: Open Terminal/Command Prompt

**Windows:**
- Press `Win + R`
- Type `cmd` or `powershell` and press Enter
- Or search for "Command Prompt" or "PowerShell" in Start Menu

**Mac/Linux:**
- Press `Cmd + Space` (Mac) or `Ctrl + Alt + T` (Linux)
- Type "Terminal" and press Enter

### Step 2: Navigate to Project Folder

Navigate to the folder where you saved or cloned this project:

**If you cloned from GitHub:**
```bash
cd movie-recs-workshop
```

**If you downloaded the project:**
```bash
cd path/to/your/project/folder
```

**Verify you're in the right folder:**
```bash
dir    # Windows
ls     # Mac/Linux
```

You should see files and folders like:
- `starter/` - Contains the starter code you'll work with
- `solution/` - Contains the complete reference solution
- `data/` - Contains the local movie data
- `README.md` - Project documentation
- `requirements.txt` - Python dependencies

### Step 3: Install Dependencies

Before running the program, you need to install the required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- `requests` - For making API calls to TMDB
- `python-dotenv` - For loading API keys from .env files (optional)

### Step 4: Set Up Your API Key (Optional but Recommended)

To use the TMDB API and get live movie data, you'll need to set up your API key:

**Easy Way: Use the Setup Script**
```bash
python setup_api_key.py
```

This script will:
- Open the TMDB API key page in your browser
- Guide you through getting your free API key
- Help you save it to `.env` or `config.py`

**Note:** If you don't set up an API key, the program will still work using the local `data/movies.json` file. However, getting a free API key gives you access to many more movies and up-to-date data!

### Step 5: Run the Program

**Start with the Starter Code (Recommended)**
```bash
python starter/recommender.py
```

This is the code you'll be working with. It has TODOs for you to complete, which will help you learn Python concepts.

**Or Check Out the Complete Solution**
```bash
python solution/recommender.py
```

This is the complete, working version. You can reference it to check your work or see how the final solution looks.

### Step 6: Use the Program

When the program starts, you'll see a welcome message and be asked for your movie mood:

```
🎬 Welcome to the Movie Night Recommender!
✨ Using real TMDB API for live movie data!
Describe your vibe (comma-separated, e.g. chill, funny, horror): 
```

Or if you're using the local file without an API key:

```
🎬 Welcome to the Movie Night Recommender!
💡 Tip: Get a free TMDB API key to use real movie data!
Describe your vibe (comma-separated, e.g. chill, funny, horror): 
```

**Enter your movie mood tags:**
- Examples: `action, comedy`
- Examples: `chill, funny, cozy`
- Examples: `horror, thriller`
- Examples: `romantic, comedy`
- Examples: `drama, emotional`

**Press Enter** to get your personalized movie recommendations!

### Step 7: View Your Recommendations

The program will:
1. Load movies from the TMDB API (if you have an API key) or from the local file
2. Score each movie based on how well it matches your mood tags
3. Show you the top 5 recommendations with details

**Example Output (with API key):**
```
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

**Example Output (without API key, using local data):**
```
[INFO] No TMDB API key found. Using local movies.json file.
Loaded 8 movies.

🍿 Your Movie Night Recommendations:

1. The Lovebirds (score: 3.0)
   Genre: Comedy
   Mood tags: funny, romantic, chill, feel-good, rom-com
   Platform: Netflix
   Description: A hilarious rom-com about a couple who accidentally witness a murder...
```

## Troubleshooting

### Problem: "python: command not found"
**Solution:**
```bash
# Try these instead:
py starter/recommender.py          # Windows
python3 starter/recommender.py     # Mac/Linux
```

### Problem: "Module not found: requests"
**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: "No API key found"
**Solution:**
- Check that `config.py` exists in the project folder
- Verify the API key is set in `config.py`
- Run: `python setup_api_key.py` to set it up

### Problem: "API request failed"
**Solution:**
- Check your internet connection
- Verify the API key is correct
- The program will automatically fall back to local movies.json

### Problem: "No movies found"
**Solution:**
- Try different mood tags (e.g., "action", "comedy", "drama")
- Check your internet connection if using API
- Verify `data/movies.json` exists if using local file

## What to Expect

### With API Key
- ✅ Fetches 20 movies from TMDB API
- ✅ Shows ratings, release dates, descriptions
- ✅ Real-time movie data from TMDB
- ✅ Many more movie options to choose from
- ✅ Requires internet connection

### Without API Key (Using Local Data)
- ✅ Uses local `data/movies.json` (8 movies)
- ✅ Still works perfectly, just fewer options
- ✅ No internet connection required
- ✅ Great for learning and testing

## Next Steps

1. **Try different mood tags to explore:**
   - `action, adventure` - Action-packed adventures
   - `comedy, family` - Family-friendly comedies
   - `horror, thriller` - Scary and suspenseful movies
   - `romantic, drama` - Emotional romantic dramas
   - `chill, cozy` - Relaxing and comfortable movies

2. **Experiment with the code:**
   - Open `starter/recommender.py` and explore the code
   - Look for TODO comments - these are sections you'll complete
   - Try adding more mood tags to the mapping
   - Modify the scoring algorithm to see how it affects recommendations
   - Read the comments to understand what each function does

3. **Learn more:**
   - Read `README.md` for full documentation and useful links
   - Check `PROJECT_STRUCTURE.md` to understand how the files work together
   - Visit the troubleshooting section in `README.md` if you encounter issues
   - Explore the `solution/recommender.py` to see the complete implementation

## Quick Commands Reference

```bash
# Navigate to your project folder
cd path/to/your/project

# Run starter code (your main working file)
python starter/recommender.py

# Run solution code (complete reference)
python solution/recommender.py

# Install dependencies
pip install -r requirements.txt

# Set up API key (if needed)
python setup_api_key.py

# Check Python version
python --version

# Check installed packages
pip list
```

## Ready to Start?

Run this command:
```bash
python starter/recommender.py
```

Then enter your mood tags when prompted! 🎬

