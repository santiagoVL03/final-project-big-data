from flask import Blueprint, make_response, jsonify
from .controller import Upload_new_comicController


upload_new_comic_bp = Blueprint('upload_new_comic', __name__)
upload_new_comic_controller = Upload_new_comicController()
@upload_new_comic_bp.route('/', methods=['GET'])
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
    result=upload_new_comic_controller.index()
    return make_response(jsonify(data=result))
      