from app.repository.hdfs.hdfs_comics import get_comic_image

class Get_comic_coverController:
    def index(self, comic_id: str) -> tuple[bytes, str]:
        return get_comic_image(comic_id)
