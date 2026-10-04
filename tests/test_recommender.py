import unittest

import recommender


class RecommenderTests(unittest.TestCase):
    def test_parse_user_tags_normalizes_and_deduplicates(self):
        tags = recommender.parse_user_tags(" Funny, action, funny , ")
        self.assertEqual(tags, {"funny", "action"})

    def test_genre_mapping_ignores_local_only_tags(self):
        genre_ids = recommender.get_genre_ids_from_tags({"funny", "chill", "action"})
        self.assertCountEqual(genre_ids, [35, 28])

    def test_score_movie_rewards_overlap_and_genre(self):
        movie = {
            "genre": "Action",
            "mood_tags": ["action", "adventure", "epic"],
        }
        self.assertEqual(recommender.score_movie(movie, {"action", "adventure"}), 3)

    def test_recommend_movies_returns_only_positive_matches(self):
        movies = [
            {"title": "A", "genre": "Comedy", "mood_tags": ["funny"]},
            {"title": "B", "genre": "Action", "mood_tags": ["action"]},
            {"title": "C", "genre": "Drama", "mood_tags": ["drama"]},
        ]
        results = recommender.recommend_movies(movies, {"funny"}, top_k=5)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1]["title"], "A")


if __name__ == "__main__":
    unittest.main()
