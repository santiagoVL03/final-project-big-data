from flask import Blueprint, make_response, jsonify, request
from .controller import Upload_new_comicController
from app.models.entities.comic import Comic

upload_new_comic_bp = Blueprint('upload_new_comic', __name__)
upload_new_comic_controller = Upload_new_comicController()
@upload_new_comic_bp.route('/', methods=['POST'], strict_slashes=False)

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
    data = request.get_json()
    comic_details = data.get('comic_details')
    if not comic_details:
        return make_response(jsonify({"error": "Comic details are required"}), 400)
      
    comic_details = Comic(
        title=comic_details.get('title'),
        author=comic_details.get('author'),
        description=comic_details.get('description'),
        date_uploaded=comic_details.get('date_uploaded'),
        comic_id=comic_details.get('comic_id')
    )
    
    if not comic_details.title or not comic_details.author or not comic_details.description:
        return make_response(jsonify({"error": "Title, author, and description are required"}), 400)
    
    cover = data.get('cover')
    content = data.get('content')
    result = upload_new_comic_controller.index(comic_details, cover, content)
    return make_response(jsonify(data=result))