import unittest
import json

from app.modules.visual.controller import VisualController


def test_index():
    visual_controller = VisualController()
    result = visual_controller.index()
    assert result == {'message': 'Hello, World!'}
