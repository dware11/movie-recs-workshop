import unittest

import advanced_recommender


class AdvancedRecommenderTests(unittest.TestCase):
    def test_sparse_cosine_similarity_identical_vectors(self):
        vector = {"1": 5.0, "2": 3.0}
        score = advanced_recommender.cosine_similarity_sparse(vector, vector)
        self.assertAlmostEqual(score, 1.0)

    def test_sparse_cosine_similarity_handles_no_overlap(self):
        score = advanced_recommender.cosine_similarity_sparse(
            {"1": 5.0},
            {"2": 5.0},
        )
        self.assertEqual(score, 0.0)

    def test_title_matching_supports_substrings(self):
        titles = ["Toy Story (1995)", "Jumanji (1995)"]
        matched, suggestions = advanced_recommender.find_best_title_match("toy story", titles)
        self.assertEqual(matched, "Toy Story (1995)")
        self.assertIn("Toy Story (1995)", suggestions)

    def test_pure_python_recommendations_rank_similar_titles(self):
        engine = {
            "mode": "pure_python",
            "movie_vectors": {
                "A": {"1": 5.0, "2": 4.0},
                "B": {"1": 5.0, "2": 4.0},
                "C": {"3": 5.0},
            },
            "movie_stats": {
                "A": {"avg_rating": 4.5, "num_ratings": 2, "genres": "Drama"},
                "B": {"avg_rating": 4.5, "num_ratings": 2, "genres": "Drama"},
                "C": {"avg_rating": 5.0, "num_ratings": 1, "genres": "Comedy"},
            },
            "movie_titles": ["A", "B", "C"],
        }
        results = advanced_recommender.get_recommendations(engine, "A", top_n=2)
        self.assertEqual(results[0]["title"], "B")
        self.assertAlmostEqual(results[0]["similarity"], 1.0)


if __name__ == "__main__":
    unittest.main()
