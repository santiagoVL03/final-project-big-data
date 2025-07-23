import unittest
import json

from app.modules.get_comic_cover.controller import Get_comic_coverController


def test_index():
    get_comic_cover_controller = Get_comic_coverController()
    result = get_comic_cover_controller.index()
    assert result == {'message': 'Hello, World!'}
