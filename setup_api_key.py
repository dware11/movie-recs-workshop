"""
API Key Setup Helper Script

Welcome! This script helps you set up your TMDB API key for the Movie Night Recommender.
It guides you through the process of getting your free API key and configuring it.

What this script does:
- Opens the TMDB API key page in your browser
- Guides you through getting your free API key
- Helps you save your API key to .env or config.py
- Makes setup easy and automated
"""

import os
import webbrowser
from pathlib import Path

def print_welcome():
    """Print welcome message and instructions."""
    print("=" * 60)
    print("🎬 Movie Night Recommender - API Key Setup")
    print("=" * 60)
    print()
    print("This script will help you set up your TMDB API key.")
    print("The API key is FREE and takes just a few minutes to get.")
    print()

def open_api_key_url():
    """Open the TMDB API key page in the user's browser."""
    api_key_url = "https://www.themoviedb.org/settings/api"
    print("Opening TMDB API key page in your browser...")
    print(f"URL: {api_key_url}")
    print()
    try:
        webbrowser.open(api_key_url)
        print("✅ Browser opened! Please follow these steps:")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically. Please visit:")
        print(f"   {api_key_url}")
    
    print()
    print("Steps to get your API key:")
    print("1. Sign up or log in to TMDB")
    print("2. Click 'Request API Key'")
    print("3. Choose 'Developer' option")
    print("4. Fill out the form (application name, etc.)")
    print("5. Copy your API key")
    print()

def get_api_key_from_user():
    """Get API key from user input."""
    print("Please paste your API key here (or press Enter to skip):")
    api_key = input("API Key: ").strip()
    return api_key

def save_api_key_to_env(api_key):
    """Save API key to .env file."""
    env_file = Path(".env")
    
    # Check if .env file exists
    if env_file.exists():
        # Read existing content
        with open(env_file, "r") as f:
            content = f.read()
        
        # Check if TMDB_API_KEY already exists
        if "TMDB_API_KEY" in content:
            print("⚠️  .env file already contains TMDB_API_KEY")
            overwrite = input("Do you want to overwrite it? (y/n): ").strip().lower()
            if overwrite != 'y':
                print("❌ API key not saved.")
                return False
            
            # Replace existing key
            lines = content.split("\n")
            new_lines = []
            for line in lines:
                if line.startswith("TMDB_API_KEY"):
                    new_lines.append(f"TMDB_API_KEY={api_key}")
                else:
                    new_lines.append(line)
            content = "\n".join(new_lines)
        else:
            # Add new key
            content += f"\nTMDB_API_KEY={api_key}\n"
    else:
        # Create new .env file
        content = f"TMDB_API_KEY={api_key}\n"
    
    # Write to .env file
    try:
        with open(env_file, "w") as f:
            f.write(content)
        print("✅ API key saved to .env file!")
        return True
    except Exception as e:
        print(f"❌ Error saving API key: {e}")
        return False

def save_api_key_to_config(api_key):
    """Save API key to config.py file."""
    config_file = Path("config.py")
    config_example = Path("config.py.example")
    
    # Check if config.py exists
    if config_file.exists():
        print("⚠️  config.py file already exists")
        overwrite = input("Do you want to overwrite it? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("❌ API key not saved.")
            return False
    else:
        # Copy from example if it exists
        if config_example.exists():
            with open(config_example, "r") as f:
                content = f.read()
            content = content.replace("your_api_key_here", api_key)
        else:
            content = f'# TMDB API Configuration\nTMDB_API_KEY = "{api_key}"\n'
    
    # Write to config.py file
    try:
        with open(config_file, "w") as f:
            f.write(f'# TMDB API Configuration\nTMDB_API_KEY = "{api_key}"\n')
        print("✅ API key saved to config.py file!")
        return True
    except Exception as e:
        print(f"❌ Error saving API key: {e}")
        return False

def main():
    """Main setup function."""
    print_welcome()
    
    # Ask if user wants to get API key
    print("Do you want to get a TMDB API key now? (y/n):")
    response = input().strip().lower()
    
    if response != 'y':
        print("❌ Setup cancelled.")
        print("You can still use the program with the local movies.json file.")
        print("To set up API key later, run this script again.")
        return
    
    # Open API key URL
    open_api_key_url()
    
    # Wait for user to get API key
    input("Press Enter when you have your API key...")
    print()
    
    # Get API key from user
    api_key = get_api_key_from_user()
    
    if not api_key:
        print("❌ No API key provided. Setup cancelled.")
        print("You can still use the program with the local movies.json file.")
        return
    
    # Ask where to save
    print()
    print("Where would you like to save your API key?")
    print("1. .env file (recommended)")
    print("2. config.py file")
    print("3. Both")
    choice = input("Enter choice (1/2/3): ").strip()
    
    success = False
    if choice == "1" or choice == "3":
        success = save_api_key_to_env(api_key) or success
    if choice == "2" or choice == "3":
        success = save_api_key_to_config(api_key) or success
    
    if success:
        print()
        print("=" * 60)
        print("✅ Setup complete!")
        print("=" * 60)
        print()
        print("You can now run the Movie Night Recommender:")
        print("  python starter/recommender.py")
        print()
        print("The program will use your API key to fetch live movie data!")
    else:
        print()
        print("❌ Setup failed. You can still use the program with local data.")
        print("To set up API key later, run this script again.")

if __name__ == "__main__":
    main()

