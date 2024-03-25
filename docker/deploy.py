from fabric import task
from pathlib import Path
from shutil import make_archive
from os import environ
from fabric import Connection

# Define the remote host IP address
DIGITAL_OCEAN_IP_ADDRESS = environ.get("DIGITAL_OCEAN_IP_ADDRESS")


@task
def upload_and_build(c):
    """
    Upload the project to the remote server and build the Docker image.

    Args:
    - c (fabric.Connection): Fabric connection object for executing commands on the remote server.
    """
    # Check if the IP address is defined
    if not DIGITAL_OCEAN_IP_ADDRESS:
        print("DIGITAL_OCEAN_IP_ADDRESS not defined")
        return

    # Create a tar archive of the 'deployment' branch
    archive_path = Path.cwd() / "project.tar"
    make_archive(str(archive_path.stem), "tar", str(Path.cwd()), "deployment")

    print("Uploading the project.....:-)...Be Patient!")
    # Upload the tar archive to the remote server
    c.put(str(archive_path), remote="/tmp/project.tar")
    print("Upload complete....:-)")

    print("Building the image.......")
    with c.cd("/tmp"):
        # Extract the uploaded archive and build the Docker image
        c.run("mkdir -p /app")
        c.run("rm -rf /app/* && tar -xf /tmp/project.tar -C /app")
        c.run("docker-compose -f /app/production.yml build")

    print("Build completed successfully.......:-)")


# Define the connection to the remote server
conn = Connection(f"root@{DIGITAL_OCEAN_IP_ADDRESS}", connect_kwargs={"password": ""})

# Execute the upload_and_build task
upload_and_build(conn)
