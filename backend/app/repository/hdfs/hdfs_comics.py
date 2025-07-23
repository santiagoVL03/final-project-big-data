from io import BytesIO
import mimetypes
from typing import cast
from app.models.entities.comic import Comic
from app.utils.ssh_conections import execute_simple_command
from hdfs import InsecureClient
import base64
import tempfile
import json

def upload_comic_to_hdfs(comic_data: Comic, cover: str, content: str) -> bool:
    from app.utils.ssh_conections import create_ssh_client, execute_remote_command, close_ssh_client

    with open("/shared/final-project-big-data/backend/app/credentials/ssh_conection.json") as f:
        config = json.load(f)

    client = create_ssh_client(
        server_ip=config["server_ip"],
        server_port=config["server_port"],
        username=config["username"],
        password=config["password"]
    )

    try:
        sftp = client.open_sftp()
        comic_id = comic_data.comic_id

        # Decodificar y guardar archivos temporales
        with tempfile.NamedTemporaryFile(delete=False) as f_cover:
            f_cover.write(base64.b64decode(cover))
            local_cover_path = f_cover.name

        with tempfile.NamedTemporaryFile(delete=False) as f_content:
            f_content.write(base64.b64decode(content))
            local_content_path = f_content.name

        with tempfile.NamedTemporaryFile(delete=False, mode="w") as f_meta:
            f_meta.write(str(comic_data.to_dict()))
            local_meta_path = f_meta.name

        # Subir archivos por SFTP
        sftp.put(local_cover_path, f"/tmp/{comic_id}_cover")
        sftp.put(local_content_path, f"/tmp/{comic_id}_content")
        sftp.put(local_meta_path, f"/tmp/{comic_id}_metadata")

        # Ejecutar comandos remotos para moverlos a HDFS
        command = f"""
            hdfs dfs -mkdir -p /comics/{comic_id} &&
            hdfs dfs -put /tmp/{comic_id}_cover /comics/{comic_id}/cover &&
            hdfs dfs -put /tmp/{comic_id}_content /comics/{comic_id}/content &&
            hdfs dfs -put /tmp/{comic_id}_metadata /comics/{comic_id}/metadata &&
            rm /tmp/{comic_id}_cover /tmp/{comic_id}_content /tmp/{comic_id}_metadata
        """
        stdout, stderr = execute_remote_command(client, command)
        print(stdout)
        if stderr:
            print(stderr)
            return False
        return True

    finally:
        close_ssh_client(client)

def get_comic_images(comic_ids: list[str]) -> list[tuple[str, str]]:
    """Get the cover images of the comics from the metadata.

    Args:
        comic_ids (list[str]): The list of comic IDs.

    Returns:
        list[tuple[str, str]]: The list of cover image paths and their corresponding comic IDs.
    """
    try:
        hdfs_client = InsecureClient('http://localhost:9870', user='hduser')
        cover_paths = []
        preview_paths = []
        
        for comic_id in comic_ids:
            if not hdfs_client.status(f'/comics/{comic_id}/content', strict=False):
                print(f"Comic ID {comic_id} does not exist in HDFS.")
                continue
            cover_paths.append(f'/comics/{comic_id}/cover')
            preview_paths.append(f'/comics/{comic_id}/content')
        if not cover_paths or not preview_paths:
            print("No valid comic IDs provided or no comics found in HDFS.")
            return []
        return list(zip(cover_paths, preview_paths))
    except:
        # Handle exceptions such as connection errors or file not found
        print("An error occurred while accessing HDFS.")
        return []
    
def get_comic_image(comic_id: str) -> tuple[bytes, str]:
    try:
        hdfs_client = InsecureClient('http://localhost:9870', user='hduser')
        hdfs_path = f'/comics/{comic_id}/cover'

        with hdfs_client.read(hdfs_path) as reader:
            reader = cast(BytesIO, reader)
            image_data = reader.read()
            if not isinstance(image_data, bytes):
                raise ValueError("Image data is not in bytes format")

        guessed_type = mimetypes.guess_type(hdfs_path)[0] 
        extension = guessed_type.split('/')[1] if guessed_type else 'png'

        return image_data, extension

    except Exception as e:
        print(f"[HDFS ERROR] {e}")
        return b'', 'png'