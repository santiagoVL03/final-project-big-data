from app.repository.producers import producer_get_comics_feed


class Get_feed_mangasController:
    def index(self):
        comic_metadata = producer_get_comics_feed.get_metadata_comics_feed()
        if comic_metadata:
            return {'success': True, 'message': 'Comics found', 'comics': [comic.to_dict() for comic in comic_metadata]}
        return {'success': False, 'message': 'No comics found'}, 404
