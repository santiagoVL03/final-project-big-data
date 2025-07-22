import unittest
import json

from app.modules.like.controller import LikeController


def test_index():
    like_controller = LikeController()
    result = like_controller.index()
    assert result == {'message': 'Hello, World!'}
