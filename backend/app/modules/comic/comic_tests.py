import unittest
import json

from app.modules.comic.controller import ComicController


def test_index():
    comic_controller = ComicController()
    result = comic_controller.index()
    assert result == {'message': 'Hello, World!'}
