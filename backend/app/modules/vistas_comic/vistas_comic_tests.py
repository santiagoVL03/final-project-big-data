import unittest
import json
from app.modules.vistas_comic.controller import Vistas_comicController

class TestVistasComic(unittest.TestCase):
    def setUp(self):
        self.controller = Vistas_comicController()

    def test_index(self):
        result = self.controller.index()
        self.assertEqual(result, {'message': 'Hello, World!'})

    def test_registrar_vista(self):
        # Simulación (con valores ficticios)
        result_json = self.controller.registrar_vista("user123", "comic456")
        result = json.loads(result_json)
        self.assertIn("status", result)
        self.assertEqual(result["status"], "ok")
