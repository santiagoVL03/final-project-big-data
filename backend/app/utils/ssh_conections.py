import paramiko
import json

def execute_simple_command(command: str) -> tuple[str, str]:
    """Execute a simple command on the local machine."""
    with open("./backend/app/credentials/ssh_conection.json") as f:
        config = json.load(f)
    client = create_ssh_client(
        server_ip=config["server_ip"],
        server_port=config["server_port"],
        username=config["username"],
        password=config["password"]
    )
    stdout, stderr = execute_remote_command(client, command)
    close_ssh_client(client)
    return stdout, stderr

def create_ssh_client(server_ip: str, server_port: int, username: str, password: str) -> paramiko.SSHClient:
    """Create an SSH client and connect to the remote server."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server_ip, port=server_port, username=username, password=password)
    return client

def execute_remote_command(ssh_client: paramiko.SSHClient, command: str) -> tuple[str, str]:
    """Execute a command on the remote server."""
    export_env = (
            'export HADOOP_HOME=/home/santiago/hadoop-3.3.2 && '
            'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 && '
            'export PATH=$HADOOP_HOME/sbin:$HADOOP_HOME/bin:$HIVE_HOME/bin:$PATH'
        )
    full_command = export_env + ' && ' + command
    stdin, stdout, stderr = ssh_client.exec_command(full_command)
    return stdout.read().decode(), stderr.read().decode()

def close_ssh_client(ssh_client: paramiko.SSHClient) -> None:
    """Close the SSH connection."""
    ssh_client.close()