from flask import send_file
from io import BytesIO
from app.repository.hdfs import hdfs_comics

class Get_comic_coverController:
    def index(self, comic_id: str):
        image_bytes, extension = hdfs_comics.get_comic_image(comic_id)

        if image_bytes:
            return send_file(
                BytesIO(image_bytes),
                mimetype=f'image/{extension}',
                as_attachment=False,
                download_name=f"{comic_id}.{extension}"
            )
        return {'success': False, 'message': 'No comic image found'}, 404
