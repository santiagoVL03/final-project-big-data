from flask import Blueprint, make_response, jsonify, request
from .controller import Get_feed_mangasController


get_feed_mangas_bp = Blueprint('get_feed_mangas', __name__)
get_feed_mangas_controller = Get_feed_mangasController()
@get_feed_mangas_bp.route('/', methods=['GET'])
def index():
    """ Example endpoint with simple greeting.
    ---
    tags:
      - Example API
    responses:
      200:
        description: A simple greeting
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                message:
                  type: string
                  example: "Hello World!"
    """
    result = get_feed_mangas_controller.index()
    return make_response(jsonify(data=result))