"""Interactive helper for saving a TMDB API key to the project's .env file."""

from getpass import getpass
from pathlib import Path
import webbrowser


PROJECT_ROOT = Path(__file__).resolve().parent
ENV_FILE = PROJECT_ROOT / ".env"
TMDB_API_URL = "https://www.themoviedb.org/settings/api"


def print_welcome():
    print("=" * 58)
    print("Movie Recommender Workshop - TMDB Setup")
    print("=" * 58)
    print()
    print("The workshop works without an API key by using local sample data.")
    print("TMDB setup is optional and enables live movie discovery.")
    print()


def open_api_key_url():
    print(f"TMDB API settings: {TMDB_API_URL}")
    try:
        webbrowser.open(TMDB_API_URL)
        print("The API settings page was opened in your browser.")
    except Exception:
        print("The browser could not be opened automatically.")
    print()


def get_api_key_from_user():
    """Read the key without echoing it back to the terminal."""
    print("Paste your TMDB API key below. Input will be hidden.")
    return getpass("API key: ").strip()


def save_api_key_to_env(api_key):
    """Create or update TMDB_API_KEY while preserving unrelated .env entries."""
    existing_lines = []
    if ENV_FILE.exists():
        try:
            existing_lines = ENV_FILE.read_text(encoding="utf-8").splitlines()
        except OSError as error:
            print(f"Could not read {ENV_FILE.name}: {error}")
            return False

    updated_lines = []
    replaced = False
    for line in existing_lines:
        if line.strip().startswith("TMDB_API_KEY="):
            updated_lines.append(f"TMDB_API_KEY={api_key}")
            replaced = True
        else:
            updated_lines.append(line)

    if not replaced:
        updated_lines.append(f"TMDB_API_KEY={api_key}")

    try:
        ENV_FILE.write_text("\n".join(updated_lines).rstrip() + "\n", encoding="utf-8")
    except OSError as error:
        print(f"Could not write {ENV_FILE.name}: {error}")
        return False

    print(f"API key saved to {ENV_FILE.name}.")
    print("That file is ignored by Git and should never be committed.")
    return True


def main():
    print_welcome()

    response = input("Set up live TMDB access now? (y/n): ").strip().lower()
    if response != "y":
        print("Setup skipped. You can still run: python recommender.py")
        return

    open_api_key_url()
    input("Press Enter after you have created/copied your API key...")
    print()

    api_key = get_api_key_from_user()
    if not api_key:
        print("No API key was provided. Nothing was changed.")
        return

    if save_api_key_to_env(api_key):
        print()
        print("Setup complete. Run: python recommender.py")


if __name__ == "__main__":
    main()
