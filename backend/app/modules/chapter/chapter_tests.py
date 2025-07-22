import unittest
import json

from app.modules.chapter.controller import ChapterController


def test_index():
    chapter_controller = ChapterController()
    result = chapter_controller.index()
    assert result == {'message': 'Hello, World!'}
