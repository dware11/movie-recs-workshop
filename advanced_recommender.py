"""
Advanced Movie Recommender (MovieLens Edition)

This is a separate "next-step" script for students who finished the basic workshop.
It demonstrates a more ML-style recommender using:
  - pandas
  - numpy
  - scikit-learn

How this differs from the basic recommender:
- Basic version: rule-based vibe matching using mood tags.
- Advanced version: collaborative filtering style similarity using real user ratings.
  We learn from patterns in many users' ratings, not just hand-written rules.
"""

from pathlib import Path
import sys
import difflib


def import_required_libraries():
    """Import required libraries with a friendly error for beginners."""
    try:
        import pandas as pd
        import numpy as np
        from sklearn.metrics.pairwise import cosine_similarity
        return pd, np, cosine_similarity
    except ModuleNotFoundError as error:
        missing_package = str(error).split("'")[1] if "'" in str(error) else "a package"
        print("Missing dependency detected.")
        print(f"Could not import: {missing_package}")
        print("Please run this command, then try again:")
        print("pip install -r requirements-advanced.txt")
        return None, None, None


PD, NP, COSINE_SIMILARITY = import_required_libraries()


PROJECT_ROOT = Path(__file__).resolve().parent
DATASET_DIR = PROJECT_ROOT / "data" / "ml-latest-small"
MOVIES_FILE = DATASET_DIR / "movies.csv"
RATINGS_FILE = DATASET_DIR / "ratings.csv"
TAGS_FILE = DATASET_DIR / "tags.csv"  # Optional for this first advanced version


def check_dataset_files():
    """Check that required MovieLens files exist."""
    missing_files = []
    for required_file in [MOVIES_FILE, RATINGS_FILE]:
        if not required_file.exists():
            missing_files.append(required_file.name)

    if missing_files:
        print("Missing dataset files for advanced recommender.")
        print("Please download MovieLens Latest Small and place files at:")
        print(f"  {DATASET_DIR}")
        print("Required files:")
        print("  - movies.csv")
        print("  - ratings.csv")
        print("Optional file:")
        print("  - tags.csv")
        print()
        print("Missing right now:")
        for name in missing_files:
            print(f"  - {name}")
        return False

    return True


def load_movielens_data():
    """
    Load MovieLens files.

    Dataset notes for students:
    - movies.csv: movie id, title, and genres
    - ratings.csv: user id, movie id, and rating (1 to 5 stars)
    - tags.csv: optional user tags, not required for this first engine
    """
    print("Loading dataset...")
    movies_df = PD.read_csv(MOVIES_FILE)
    ratings_df = PD.read_csv(RATINGS_FILE)

    if TAGS_FILE.exists():
        tags_df = PD.read_csv(TAGS_FILE)
    else:
        tags_df = PD.DataFrame()

    required_movie_columns = {"movieId", "title", "genres"}
    required_rating_columns = {"userId", "movieId", "rating"}

    if not required_movie_columns.issubset(movies_df.columns):
        print("movies.csv is missing expected columns.")
        return None, None, None

    if not required_rating_columns.issubset(ratings_df.columns):
        print("ratings.csv is missing expected columns.")
        return None, None, None

    return movies_df, ratings_df, tags_df


def build_recommender_engine(movies_df, ratings_df, min_ratings=20):
    """
    Build a collaborative-filtering style engine using movie-to-movie similarity.

    Beginner concept:
    - We build a user-item matrix:
      rows = movies, columns = users, values = ratings.
    - Then we compare movie vectors with cosine similarity.
    - If two movies get similar patterns of ratings from many users,
      they are considered similar.
    """
    print("Building recommendation engine...")

    # Join ratings with movie titles so we can work with readable names.
    ratings_with_titles = ratings_df.merge(
        movies_df[["movieId", "title", "genres"]],
        on="movieId",
        how="left",
    )

    # Remove entries without a title just to be safe.
    ratings_with_titles = ratings_with_titles.dropna(subset=["title"])

    # Filter out movies with very few ratings to reduce noisy similarity scores.
    rating_counts = ratings_with_titles.groupby("title")["rating"].count()
    popular_titles = rating_counts[rating_counts >= min_ratings].index

    filtered_ratings = ratings_with_titles[ratings_with_titles["title"].isin(popular_titles)]

    # If the threshold is too strict (unlikely, but possible), relax it.
    if filtered_ratings.empty:
        relaxed_titles = rating_counts[rating_counts >= 5].index
        filtered_ratings = ratings_with_titles[ratings_with_titles["title"].isin(relaxed_titles)]

    if filtered_ratings.empty:
        print("Not enough rating data to build recommendations.")
        return None

    # User-item matrix:
    # - each movie is represented by a vector of user ratings
    # - missing ratings become 0
    user_item_matrix = filtered_ratings.pivot_table(
        index="title",
        columns="userId",
        values="rating",
    ).fillna(0)

    if user_item_matrix.empty:
        print("Could not create user-item matrix.")
        return None

    # Cosine similarity gives a score from 0 to 1 (closer to 1 means more similar).
    similarity_matrix = COSINE_SIMILARITY(user_item_matrix.values)
    similarity_df = PD.DataFrame(
        similarity_matrix,
        index=user_item_matrix.index,
        columns=user_item_matrix.index,
    )

    # Metadata for nicer output
    movie_stats = ratings_with_titles.groupby("title").agg(
        avg_rating=("rating", "mean"),
        num_ratings=("rating", "count"),
        genres=("genres", "first"),
    )

    return {
        "similarity_df": similarity_df,
        "movie_stats": movie_stats,
        "movie_titles": list(similarity_df.index),
    }


def find_best_title_match(user_input_title, available_titles):
    """
    Find the best matching title for user input.

    Matching strategy:
    1) exact case-insensitive match
    2) substring match
    3) close string match (difflib)
    """
    cleaned_input = user_input_title.strip().lower()
    if not cleaned_input:
        return None, []

    title_lookup = {title.lower(): title for title in available_titles}

    if cleaned_input in title_lookup:
        return title_lookup[cleaned_input], []

    substring_matches = [title for title in available_titles if cleaned_input in title.lower()]
    if substring_matches:
        return substring_matches[0], substring_matches[:10]

    lower_titles = list(title_lookup.keys())
    close_lower = difflib.get_close_matches(cleaned_input, lower_titles, n=5, cutoff=0.6)
    close_matches = [title_lookup[title] for title in close_lower]

    if close_matches:
        return close_matches[0], close_matches

    return None, []


def get_recommendations(engine, input_title, top_n=5):
    """Return top-N similar movies for the selected title."""
    similarity_df = engine["similarity_df"]
    movie_stats = engine["movie_stats"]

    if input_title not in similarity_df.index:
        return []

    similarity_scores = similarity_df[input_title].sort_values(ascending=False)
    similarity_scores = similarity_scores.drop(index=input_title, errors="ignore")

    recommendations = []
    for title, score in similarity_scores.items():
        # Skip very weak similarities to keep output useful.
        if score <= 0:
            continue

        stats = movie_stats.loc[title]
        recommendations.append(
            {
                "title": title,
                "similarity": float(score),
                "avg_rating": float(stats["avg_rating"]),
                "num_ratings": int(stats["num_ratings"]),
                "genres": stats["genres"],
            }
        )

        if len(recommendations) == top_n:
            break

    return recommendations


def print_recommendations(input_title, recommendations):
    """Print recommendation results in a beginner-friendly format."""
    print()
    print(f"Because you liked: {input_title}")
    print("Here are your recommendations:")
    print()

    if not recommendations:
        print("No similar movies found yet for that title.")
        print("Try another movie with more ratings in the dataset.")
        return

    for index, rec in enumerate(recommendations, start=1):
        confidence_percent = NP.clip(rec["similarity"] * 100, 0, 100)
        print(f"{index}. {rec['title']}")
        print(f"   Similarity score: {confidence_percent:.1f}%")
        print(f"   Average rating: {rec['avg_rating']:.2f} / 5")
        print(f"   Number of ratings: {rec['num_ratings']}")
        print(f"   Genres: {rec['genres']}")
        print()


def main():
    """Run the advanced recommender end-to-end."""
    if PD is None or NP is None or COSINE_SIMILARITY is None:
        return

    print("Advanced Movie Recommender (MovieLens)")
    print("-------------------------------------")

    if not check_dataset_files():
        return

    movies_df, ratings_df, _tags_df = load_movielens_data()
    if movies_df is None or ratings_df is None:
        return

    engine = build_recommender_engine(movies_df, ratings_df, min_ratings=20)
    if engine is None:
        return

    print("Engine ready.")
    print()

    user_input_title = input("Enter a movie title you like: ").strip()
    if not user_input_title:
        print("Please enter a movie title (for example: Toy Story (1995)).")
        return

    matched_title, suggestions = find_best_title_match(
        user_input_title,
        engine["movie_titles"],
    )

    if not matched_title:
        print("No matching movie title found.")
        print("Try a more complete title, including the year if possible.")
        return

    if matched_title.lower() != user_input_title.lower() and suggestions:
        print(f'Using closest match: "{matched_title}"')

    recommendations = get_recommendations(engine, matched_title, top_n=5)
    print_recommendations(matched_title, recommendations)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("Stopped by user.")
        sys.exit(0)
