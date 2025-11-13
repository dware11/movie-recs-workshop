# GitHub Setup Guide — Sharing Your Project

This guide will help you share your Movie Night Recommender project on GitHub. GitHub is a great way to showcase your work, collaborate with others, and keep track of your code changes.

## What is GitHub?

GitHub is a platform where you can store and share your code. It's like Google Drive, but specifically for code projects. You can:
- Save your code online
- Share your project with others
- Keep track of changes you make
- Collaborate with other developers
- Showcase your work in your portfolio

## What Files Should Be on GitHub?

### File:
- `.gitignore` - Tells GitHub which files to ignore
- `README.md` - Project documentation
- `START_HERE.md` - Quick start guide
- `PROJECT_STRUCTURE.md` - Project documentation
- `requirements.txt` - Python dependencies
- `config.py.example` - Template for API key (safe to share)
- `setup_api_key.py` - API key setup helper
- `starter/recommender.py` - Starter code
- `solution/recommender.py` - Complete reference solution
- `data/movies.json` - Local movie data

### Files That Should NOT Be Shared ❌
- `config.py` - Your API key (kept private for security)
- `.env` - Your environment variables (kept private)
- `__pycache__/` - Python cache files (automatically generated, not needed)

**Why?** Your API key is like a password - you don't want to share it publicly. The `.gitignore` file automatically prevents these sensitive files from being uploaded.

// 

### Method 3: Using Git Commands

If you have Git installed and set up:

```bash
# 1. Initialize Git (if not already done)
git init

# 2. Add all files (except those in .gitignore)
git add .

# 3. Create your first commit
git commit -m "Initial commit: Movie Night Recommender project"

# 4. Create repository on GitHub first (using web interface)
# Then add the remote and push:
git remote add origin https://github.com/YOUR_USERNAME/movie-recs-workshop.git
git branch -M main
git push -u origin main
```

## ✅ Verify Your Upload

After uploading, check your GitHub repository to make sure:
- ✅ `config.py` is NOT in the repository (this is correct!)
- ✅ `config.py.example` IS in the repository (this is safe to share)
- ✅ All your code files are present
- ✅ All documentation files are present
- ✅ `setup_api_key.py` is included

## 📝 Customizing Your Repository (Optional)

### Add Topics/Tags

Topics help others discover your project. On your GitHub repository page:
1. Click the gear icon next to "About"
2. Add topics like: `python`, `movie-recommender`, `tmdb-api`, `beginner-friendly`, `api-integration`
3. Click "Save changes"

### Add a Description

Add a description to help others understand your project:
1. Click the gear icon next to "About"
2. Add a description like: "A Python movie recommendation system using TMDB API"
3. Click "Save changes"

### Update README.md (Optional)

If you want to update the clone URL in README.md:
1. Go to your repository on GitHub
2. Copy the repository URL
3. Edit README.md in your local project
4. Update the clone URL to match your repository
5. Commit and push the changes

## 🔒 Security: Keeping Your API Key Safe

### Why API Keys Should Stay Private

Your API key is like a password - it gives access to the TMDB API. You should never share it publicly because:
- Others could use your API key
- You might hit rate limits
- You could be charged if the API had usage limits

### What's Safe to Share ✅

- `config.py.example` - Template file (contains no real keys, just placeholder text)
- All code files - No API keys are stored in the code
- Documentation - Setup instructions are safe to share
- `setup_api_key.py` - Helper script is safe to share

### What Should Stay Private ❌

- `config.py` - Your actual API key (automatically ignored by `.gitignore`)
- `.env` - Your environment variables (automatically ignored)

### For Others Using Your Project

When someone clones or downloads your repository:
1. They'll need to get their own TMDB API key (it's free!)
2. They can use `python setup_api_key.py` to set it up easily
3. They can use `config.py.example` as a template
4. Their `config.py` file will stay on their computer (not uploaded to GitHub)

## 📋 Quick Reference

### Clone a Repository
If someone shares their project with you:
```bash
git clone https://github.com/USERNAME/movie-recs-workshop.git
cd movie-recs-workshop
```

### Set Up the Project
After cloning or downloading:
```bash
# Install dependencies
pip install -r requirements.txt

# Set up your API key (guided setup)
python setup_api_key.py

# Run the program
python starter/recommender.py
```

### Update Your Repository
After making changes to your code:
```bash
# Stage your changes
git add .

# Commit your changes with a message
git commit -m "Description of what you changed"

# Push to GitHub
git push
```

## 🎯 Checklist: Is Your Repository Ready?

Before sharing on GitHub, make sure:
- ✅ All your code files are ready
- ✅ `config.py` is NOT in the repository (checked by `.gitignore`)
- ✅ `config.py.example` IS in the repository (safe template file)
- ✅ README.md explains the project
- ✅ `setup_api_key.py` is included
- ✅ `.gitignore` is properly configured
- ✅ All documentation files are present
- ✅ Your code runs without errors

## 📚 Additional Resources

- **GitHub Documentation**: https://docs.github.com/
- **Git Documentation**: https://git-scm.com/doc
- **TMDB API**: https://www.themoviedb.org/settings/api
- **Project README**: See `README.md` for more information

## 🆘 Troubleshooting

### Problem: `config.py` is showing in git status

**What this means**: Git is trying to track your API key file.

**Solution**: 
1. Check that `config.py` is listed in `.gitignore`
2. If it was already committed, remove it:
   ```bash
   git rm --cached config.py
   git commit -m "Remove config.py from repository"
   ```

### Problem: Can't push to GitHub

**Possible causes**:
1. **Authentication issue**: You need to sign in to GitHub
2. **Repository doesn't exist**: Create the repository on GitHub first
3. **Remote not set**: Make sure you've added the remote repository

**Solution**:
1. Check that you've added the remote:
   ```bash
   git remote -v
   ```
2. Verify you're signed in to GitHub
3. Make sure the repository exists on GitHub
4. Try using GitHub Desktop instead (easier for beginners)

### Problem: API key not working for others

**Solution**:
1. Make sure `setup_api_key.py` is in the repository
2. Verify README.md has clear setup instructions
3. Check that `config.py.example` is present
4. Remind others that they need to get their own free API key from TMDB

## 💡 Tips for Using GitHub

### Making Changes
- Always test your code before pushing to GitHub
- Write clear commit messages describing what you changed
- Push your changes regularly to save your work online

### Sharing Your Project
- Add a good description so others understand what your project does
- Use topics/tags to help others find your project
- Keep your README.md up to date with clear instructions

### Learning More
- GitHub has great tutorials for beginners
- You can learn Git commands gradually
- GitHub Desktop makes it easier if you're just starting out

---

**Remember**: GitHub is a great way to showcase your coding projects and learn from others. Don't worry if it seems complicated at first - start with GitHub Desktop and you'll learn as you go!

