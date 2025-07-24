from flask import Blueprint, make_response, jsonify, request
from .controller import Get_comic_coverController


get_comic_cover_bp = Blueprint('get_comic_cover', __name__)
get_comic_cover_controller = Get_comic_coverController()

@get_comic_cover_bp.route('/', methods=['GET'])
def index():
    """ Get comic cover image endpoint.
    ---
    tags:
      - Comic API
    parameters:
      - name: comic_id
        in: query
        type: string
        required: true
        description: The ID of the comic
    responses:
      200:
        description: Comic cover image
        content:
          image/png:
            schema:
              type: string
              format: binary
          image/jpeg:
            schema:
              type: string
              format: binary
      404:
        description: Comic not found
    """
    comic_id = request.args.get('comic_id')
    if not comic_id:
        return make_response("Comic ID is required", 400)
    
    result = get_comic_cover_controller.index(comic_id)
    
    # If result is a tuple (image_data, extension), create proper response
    if isinstance(result, tuple) and len(result) == 2:
        image_data, extension = result
        if image_data:  # Check if image data is not empty
            response = make_response(image_data)
            response.headers['Content-Type'] = f'image/{extension}'
            return response
    
    # Return 404 if no image found
    return make_response("Comic cover not found", 404)