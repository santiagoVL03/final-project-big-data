import unittest
import json

from app.modules.get_feed_mangas.controller import Get_feed_mangasController


def test_index():
    get_feed_mangas_controller = Get_feed_mangasController()
    result = get_feed_mangas_controller.index()
    assert result == {'message': 'Hello, World!'}
