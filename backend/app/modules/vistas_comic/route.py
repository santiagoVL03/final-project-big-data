from flask import Blueprint, request, make_response, jsonify
from .controller import Vistas_comicController
import json

vistas_comic_bp = Blueprint('vistas_comic', __name__)
vistas_comic_controller = Vistas_comicController()

@vistas_comic_bp.route('/', methods=['GET'])
def index():
    result = vistas_comic_controller.index()
    return make_response(jsonify(data=result))

@vistas_comic_bp.route('/registrar', methods=['POST'])
def registrar_vista():
    data = request.get_json()
    user_id = data.get('user_id')
    comic_id = data.get('comic_id')

    if not user_id or not comic_id:
        return make_response(jsonify({"error": "Faltan campos obligatorios: user_id y comic_id"}), 400)

    result = vistas_comic_controller.registrar_vista(user_id, comic_id)
    return make_response(jsonify(data=json.loads(result)))
