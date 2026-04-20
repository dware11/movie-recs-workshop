"""
Advanced Movie Recommender (MovieLens Edition)

This is a separate "next-step" script for students who finished the basic workshop.
It demonstrates a more ML-style recommender using collaborative filtering ideas.

Important:
- It tries a data-science path first (pandas + scikit-learn).
- If those libraries are blocked or unavailable, it falls back to a pure-Python
  collaborative-filtering path so the workshop can still run.
"""

from pathlib import Path
import csv
import difflib
import math
import sys


def import_optional_libraries():
    """
    Try importing data-science libraries.

    Returns:
        dict with keys:
            available: bool
            pd: pandas module or None
            cosine_similarity: sklearn cosine function or None
            error: exception text when import fails
    """
    try:
        import pandas as pd
        from sklearn.metrics.pairwise import cosine_similarity

        return {
            "available": True,
            "pd": pd,
            "cosine_similarity": cosine_similarity,
            "error": "",
        }
    except Exception as error:  # Handles both missing packages and policy blocks
        return {
            "available": False,
            "pd": None,
            "cosine_similarity": None,
            "error": str(error),
        }


LIBS = import_optional_libraries()
PD = LIBS["pd"]
COSINE_SIMILARITY = LIBS["cosine_similarity"]


PROJECT_ROOT = Path(__file__).resolve().parent
DATASET_DIR = PROJECT_ROOT / "data" / "ml-latest-small"
MOVIES_FILE = DATASET_DIR / "movies.csv"
RATINGS_FILE = DATASET_DIR / "ratings.csv"
TAGS_FILE = DATASET_DIR / "tags.csv"  # Optional in this version


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


def cosine_similarity_sparse(vector_a, vector_b):
    """
    Cosine similarity for sparse vectors represented as dicts.
    Example vector: {user_id: rating, ...}
    """
    if not vector_a or not vector_b:
        return 0.0

    dot_product = 0.0
    for key, value_a in vector_a.items():
        value_b = vector_b.get(key)
        if value_b is not None:
            dot_product += value_a * value_b

    norm_a = math.sqrt(sum(value * value for value in vector_a.values()))
    norm_b = math.sqrt(sum(value * value for value in vector_b.values()))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def load_movielens_data_pandas():
    """Load MovieLens files with pandas."""
    print("Loading dataset...")
    movies_df = PD.read_csv(MOVIES_FILE)
    ratings_df = PD.read_csv(RATINGS_FILE)

    required_movie_columns = {"movieId", "title", "genres"}
    required_rating_columns = {"userId", "movieId", "rating"}

    if not required_movie_columns.issubset(movies_df.columns):
        print("movies.csv is missing expected columns.")
        return None, None

    if not required_rating_columns.issubset(ratings_df.columns):
        print("ratings.csv is missing expected columns.")
        return None, None

    return movies_df, ratings_df


def build_recommender_engine_pandas(movies_df, ratings_df, min_ratings=20):
    """
    Build collaborative-filtering style engine with pandas + scikit-learn.

    Beginner concept:
    - Build a user-item matrix:
      rows = movies, columns = users, values = ratings.
    - Compare movie vectors with cosine similarity.
    """
    print("Building recommendation engine...")

    ratings_with_titles = ratings_df.merge(
        movies_df[["movieId", "title", "genres"]],
        on="movieId",
        how="left",
    ).dropna(subset=["title"])

    rating_counts = ratings_with_titles.groupby("title")["rating"].count()
    popular_titles = rating_counts[rating_counts >= min_ratings].index
    filtered_ratings = ratings_with_titles[ratings_with_titles["title"].isin(popular_titles)]

    if filtered_ratings.empty:
        relaxed_titles = rating_counts[rating_counts >= 5].index
        filtered_ratings = ratings_with_titles[ratings_with_titles["title"].isin(relaxed_titles)]

    if filtered_ratings.empty:
        print("Not enough rating data to build recommendations.")
        return None

    user_item_matrix = filtered_ratings.pivot_table(
        index="title",
        columns="userId",
        values="rating",
    ).fillna(0)

    if user_item_matrix.empty:
        print("Could not create user-item matrix.")
        return None

    similarity_matrix = COSINE_SIMILARITY(user_item_matrix.values)
    similarity_df = PD.DataFrame(
        similarity_matrix,
        index=user_item_matrix.index,
        columns=user_item_matrix.index,
    )

    movie_stats = ratings_with_titles.groupby("title").agg(
        avg_rating=("rating", "mean"),
        num_ratings=("rating", "count"),
        genres=("genres", "first"),
    )

    return {
        "mode": "pandas",
        "similarity_df": similarity_df,
        "movie_stats": movie_stats,
        "movie_titles": list(similarity_df.index),
    }


def load_movielens_data_pure_python():
    """
    Load MovieLens files using only Python's standard library.
    This path is used when pandas/sklearn are unavailable.
    """
    print("Loading dataset...")

    movie_id_to_title = {}
    movie_title_to_genres = {}
    with open(MOVIES_FILE, "r", encoding="utf-8", newline="") as movies_file:
        reader = csv.DictReader(movies_file)
        required_columns = {"movieId", "title", "genres"}
        if not required_columns.issubset(reader.fieldnames or []):
            print("movies.csv is missing expected columns.")
            return None

        for row in reader:
            movie_id = row["movieId"].strip()
            title = row["title"].strip()
            genres = row["genres"].strip()
            movie_id_to_title[movie_id] = title
            movie_title_to_genres[title] = genres

    ratings_rows = []
    with open(RATINGS_FILE, "r", encoding="utf-8", newline="") as ratings_file:
        reader = csv.DictReader(ratings_file)
        required_columns = {"userId", "movieId", "rating"}
        if not required_columns.issubset(reader.fieldnames or []):
            print("ratings.csv is missing expected columns.")
            return None

        for row in reader:
            movie_id = row["movieId"].strip()
            title = movie_id_to_title.get(movie_id)
            if not title:
                continue

            user_id = row["userId"].strip()
            try:
                rating = float(row["rating"])
            except ValueError:
                continue

            ratings_rows.append((user_id, title, rating))

    return {
        "movie_title_to_genres": movie_title_to_genres,
        "ratings_rows": ratings_rows,
    }


def build_recommender_engine_pure_python(data, min_ratings=20):
    """Build collaborative-filtering style engine using pure Python."""
    print("Building recommendation engine...")

    ratings_rows = data["ratings_rows"]
    movie_title_to_genres = data["movie_title_to_genres"]

    ratings_count = {}
    ratings_sum = {}
    movie_user_ratings = {}

    for user_id, title, rating in ratings_rows:
        ratings_count[title] = ratings_count.get(title, 0) + 1
        ratings_sum[title] = ratings_sum.get(title, 0.0) + rating
        movie_user_ratings.setdefault(title, {})[user_id] = rating

    filtered_titles = [title for title, count in ratings_count.items() if count >= min_ratings]
    if not filtered_titles:
        filtered_titles = [title for title, count in ratings_count.items() if count >= 5]

    if not filtered_titles:
        print("Not enough rating data to build recommendations.")
        return None

    movie_stats = {}
    for title, count in ratings_count.items():
        movie_stats[title] = {
            "avg_rating": ratings_sum[title] / count if count else 0.0,
            "num_ratings": count,
            "genres": movie_title_to_genres.get(title, "(no genres listed)"),
        }

    return {
        "mode": "pure_python",
        "movie_vectors": {title: movie_user_ratings[title] for title in filtered_titles},
        "movie_stats": movie_stats,
        "movie_titles": filtered_titles,
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
    movie_stats = engine["movie_stats"]
    recommendations = []

    if engine["mode"] == "pandas":
        similarity_df = engine["similarity_df"]
        if input_title not in similarity_df.index:
            return []

        similarity_scores = similarity_df[input_title].sort_values(ascending=False)
        similarity_scores = similarity_scores.drop(index=input_title, errors="ignore")

        for title, score in similarity_scores.items():
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
    else:
        movie_vectors = engine["movie_vectors"]
        input_vector = movie_vectors.get(input_title)
        if not input_vector:
            return []

        scored_titles = []
        for title, vector in movie_vectors.items():
            if title == input_title:
                continue
            score = cosine_similarity_sparse(input_vector, vector)
            if score > 0:
                scored_titles.append((title, score))

        scored_titles.sort(key=lambda item: item[1], reverse=True)

        for title, score in scored_titles[:top_n]:
            stats = movie_stats.get(title, {})
            recommendations.append(
                {
                    "title": title,
                    "similarity": float(score),
                    "avg_rating": float(stats.get("avg_rating", 0.0)),
                    "num_ratings": int(stats.get("num_ratings", 0)),
                    "genres": stats.get("genres", "(no genres listed)"),
                }
            )

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
        confidence_percent = max(0.0, min(100.0, rec["similarity"] * 100))
        print(f"{index}. {rec['title']}")
        print(f"   Similarity score: {confidence_percent:.1f}%")
        print(f"   Average rating: {rec['avg_rating']:.2f} / 5")
        print(f"   Number of ratings: {rec['num_ratings']}")
        print(f"   Genres: {rec['genres']}")
        print()


def get_example_titles(available_titles, count=5):
    """Return a small sample of titles to help beginners enter valid input."""
    if not available_titles:
        return []
    return sorted(available_titles)[:count]


def main():
    """Run the advanced recommender end-to-end."""
    print("Advanced Movie Recommender (MovieLens)")
    print("-------------------------------------")

    if not check_dataset_files():
        return

    if LIBS["available"]:
        movies_df, ratings_df = load_movielens_data_pandas()
        if movies_df is None or ratings_df is None:
            return

        engine = build_recommender_engine_pandas(movies_df, ratings_df, min_ratings=20)
        if engine is None:
            return
    else:
        print("Data science libraries are unavailable or blocked on this machine.")
        print("Using pure Python fallback mode.")
        print("Reason:", LIBS["error"])
        print("Tip: If allowed, install advanced packages with:")
        print("  pip install -r requirements-advanced.txt")
        print()

        data = load_movielens_data_pure_python()
        if data is None:
            return

        engine = build_recommender_engine_pure_python(data, min_ratings=20)
        if engine is None:
            return

    print("Engine ready.")
    print()
    print("Tip: MovieLens titles usually include the year, like 'Toy Story (1995)'.")
    print("Type 'q' to quit.")
    example_titles = get_example_titles(engine["movie_titles"], count=5)
    if example_titles:
        print("Examples you can try:")
        for title in example_titles:
            print(f"  - {title}")
    print()

    while True:
        user_input_title = input("Enter a movie title you like (or 'q' to quit): ").strip()

        if user_input_title.lower() in {"q", "quit", "exit"}:
            print("Thanks for exploring the advanced recommender. Goodbye!")
            break

        if not user_input_title:
            print("Please enter a movie title (for example: Toy Story (1995)).")
            print()
            continue

        matched_title, suggestions = find_best_title_match(
            user_input_title,
            engine["movie_titles"],
        )

        if not matched_title:
            print("No matching movie title found.")
            print("Try a more complete title, including the year if possible.")
            if example_titles:
                print("Here are some valid examples:")
                for title in example_titles:
                    print(f"  - {title}")
            print()
            continue

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
