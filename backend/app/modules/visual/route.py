from flask import Blueprint, make_response, jsonify
from .controller import VisualController


visual_bp = Blueprint('visual', __name__)
visual_controller = VisualController()
@visual_bp.route('/', methods=['GET'])
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
    result=visual_controller.index()
    return make_response(jsonify(data=result))
      