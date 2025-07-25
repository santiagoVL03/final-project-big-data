import app.repository.producers.producer_visitas_comic as producers
import json

class Vistas_comicController:
    def index(self):
        return {'message': 'Hello, World!'}

    def registrar_vista(self, user_id: str, comic_id: str):
        try:
            exito = producers.enviar_vista_kafka(user_id=user_id, comic_id=comic_id)

            if not exito:
                return json.dumps({"error": "Error al enviar evento de vista"}), 500

            return json.dumps({
                "status": "ok",
                "message": "Vista registrada correctamente",
                "comic_id": comic_id
            })
        except Exception as e:
            return json.dumps({"error": str(e)}), 500
