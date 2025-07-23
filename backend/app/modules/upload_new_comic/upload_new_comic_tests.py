import unittest
import json

from app.modules.upload_new_comic.controller import Upload_new_comicController


def test_index():
    upload_new_comic_controller = Upload_new_comicController()
    result = upload_new_comic_controller.index()
    assert result == {'message': 'Hello, World!'}
