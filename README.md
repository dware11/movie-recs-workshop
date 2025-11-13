# 🎬 AI Movie Night Recommender — Python + API Project

Build your own movie recommendation system in Python!  
This beginner-friendly project helps you create a simple “AI” movie recommender with **optional TMDB (The Movie Database) API integration**. You’ll practice Python fundamentals while building something fun and useful.

> **🚀 New to this project?**  
> Start with [START_HERE.md](START_HERE.md) for a gentle, step-by-step introduction.

---

## 📚 What You’ll Learn

- Python basics: variables, lists, dictionaries, sets, loops, functions  
- How JSON works and how to read it from a file  
- How APIs work and how to call them with `requests.get()`  
- How to rank and sort data to make recommendations  
- How to handle errors and fall back to local data when an API fails  
- “Scale-up” ideas for using real user data and more advanced logic  

---

## ✨ Project Features

- Uses your “movie night vibe” (e.g., `chill, funny, horror`) to suggest movies  
- **Optional** live data from the TMDB API  
- Automatic fallback to local `data/movies.json` if there’s no API key or the API fails  
- Maps mood tags to genres and aliases (e.g., `funny` → comedy)  
- Shows ratings, release dates, and descriptions (when using TMDB)  
- Works **with or without** an API key

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/movie-recs-workshop.git
cd movie-recs-workshop

