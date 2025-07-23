from flask import Blueprint, make_response, jsonify, request
from .controller import Get_comic_coverController


get_comic_cover_bp = Blueprint('get_comic_cover', __name__)
get_comic_cover_controller = Get_comic_coverController()
@get_comic_cover_bp.route('/', methods=['GET'])
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
    comic_id = request.args.get('comic_id') or ""
    result = get_comic_cover_controller.index(comic_id)
    return result if isinstance(result, tuple) else make_response(jsonify(result), 404)