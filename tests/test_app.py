from pathlib import Path
import tempfile
import unittest

import database
from app import app


ROOT = Path(__file__).resolve().parents[1]


class AppTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory()
        database.DB_PATH = Path(self.temp_directory.name) / "test.db"
        database.init_db()
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def tearDown(self) -> None:
        self.temp_directory.cleanup()

    def test_words_endpoint_returns_seed_data(self) -> None:
        response = self.client.get("/api/palavras")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.get_json()), 70)
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")

    def test_valid_score_is_saved(self) -> None:
        response = self.client.post(
            "/api/placar", json={"nome": "Carys", "pontos": 120}
        )
        self.assertEqual(response.status_code, 200)
        scores = self.client.get("/api/placar").get_json()
        self.assertEqual(scores[0]["nome"], "Carys")
        self.assertEqual(scores[0]["pontos"], 120)

    def test_invalid_scores_are_rejected(self) -> None:
        for score in (-1, 1_000_001, "120", True, None):
            with self.subTest(score=score):
                response = self.client.post(
                    "/api/placar", json={"nome": "Player", "pontos": score}
                )
                self.assertEqual(response.status_code, 400)

    def test_control_characters_are_removed_from_name(self) -> None:
        self.client.post(
            "/api/placar", json={"nome": "A\nB\u0000C", "pontos": 10}
        )
        scores = self.client.get("/api/placar").get_json()
        self.assertEqual(scores[0]["nome"], "ABC")

    def test_leaderboard_name_is_not_rendered_with_inner_html(self) -> None:
        source = (ROOT / "static/game.js").read_text(encoding="utf-8")
        self.assertNotIn("${item.nome}", source)
        self.assertIn("document.createTextNode(item.nome)", source)


if __name__ == "__main__":
    unittest.main()
