class Comic:
    def __init__(self, 
                 title: str, 
                 author: str, 
                 description: str,
                 date_uploaded: str = str(),
                 comic_id: str = str()
                 ):
        self.title = title
        self.author = author
        self.description = description
        self.date_uploaded = date_uploaded
        self.comic_id = comic_id
        if self.date_uploaded is None:
            from datetime import datetime
            self.date_uploaded = datetime.now().isoformat()

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "content": self.description,
            "date_uploaded": self.date_uploaded,
            "comic_id": self.comic_id
        }

class Chapter:
    def __init__(self, 
                 title, 
                 comic_id, 
                 comic_name,
                 content, 
                 date_uploaded=None):
        self.title = title
        self.comic_id = comic_id
        self.comic_name = comic_name
        self.content = content
        self.date_uploaded = date_uploaded

    def to_dict(self):
        return {
            "title": self.title,
            "comic_id": self.comic_id,
            "comic_name": self.comic_name,
            "content": self.content,
            "date_uploaded": self.date_uploaded
        }