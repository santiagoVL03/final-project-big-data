from app.models.entities.comic import Comic
from app.utils.ssh_conections import execute_simple_command

def upload_comic_to_hdfs(comic_data: Comic, cover: str, content: str) -> bool:
    # Lógica para subir un cómic al HDFS
    command = f"""
    hdfs dfs -mkdir -p /comics/{comic_data.comic_id} &&
    echo '{cover}' | base64 -d | hdfs dfs -put - /comics/{comic_data.comic_id}/cover &&
    echo '{content}' | base64 -d | hdfs dfs -put - /comics/{comic_data.comic_id}/content &&
    echo '{comic_data.to_dict()}' | hdfs dfs -put - /comics/{comic_data.comic_id}/metadata
    """
    stdout, stderr = execute_simple_command(command)
    if stderr:
        print(f"Error uploading comic to HDFS: {stderr}")
        return False
    return True
