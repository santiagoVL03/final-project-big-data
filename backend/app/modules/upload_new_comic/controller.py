import app.repository.producers.producer_upload_comic as producers
from app.repository.hdfs.hdfs_comics import upload_comic_to_hdfs
from app.models.entities.comic import Comic

import json

class Upload_new_comicController:
    def index(self, comic_details: Comic, cover: str, content: str):
        """_summary_
        Controller method to handle the upload of a new comic.
        Args:
            comic_details (comic_models.Comic): The details of the comic to upload.
            cover (str): The cover image of the comic it must be a base64 encoded string.
            content (str): The content of the comic it must be a base64 encoded string. 

        Returns:
            _type_: _description_
        """
        result_kafka = producers.upload_new_comic(
            comic_data=comic_details
        )
        
        if not result_kafka:
            return json.dumps({"error": "Failed to upload comic to Kafka"}), 500
        
        # For now we will not upload to HDFS, but we can uncomment the following lines to enable it.
        # Uncomment the following lines to enable HDFS upload
        # if not cover or not content:
        #     return json.dumps({"error": "Cover and content must be provided"}), 400

        result_upload_comic_hdfs = upload_comic_to_hdfs(
            comic_data=comic_details,
            cover=cover,
            content=content
        )

        # if not result_upload_comic_hdfs:
        #     return json.dumps({"error": "Failed to upload comic to HDFS"}), 500

        json_result = json.dumps({
            "status": "success",
            "code": 200,
            "message": "Comic uploaded successfully",
            "comic_id": comic_details.comic_id
        })
        print(json_result)  # Debugging output
        return json_result