import io
import logging
import os
import re
import tarfile
from pathlib import Path
from typing import Generator

import docker
from docker.client import DockerClient
from docker.models.containers import Container
from docker.models.images import Image
from docker.utils.json_stream import json_stream

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(f"pyfixm-build")


def main():
    docker_client: DockerClient = docker.from_env()
    image = build_image(docker_client)
    extract_files(docker_client, image)


def build_image(docker_client: DockerClient) -> Image:
    resp = docker_client.api.build(path=".", rm=True, tag='pyfixm')

    # noinspection PyTypeChecker
    image_id: str = None
    for chunk in json_stream(resp):
        if 'error' in chunk:
            message = f"Error while building Dockerfile for pyfixm:\n" \
                      f"{chunk['error']}"
            logger.error(message)
            raise DockerBuildError(message)

        elif 'stream' in chunk:
            logger.info(chunk['stream'].rstrip('\n'))
            # Taken from the high level API implementation of build
            match = re.search(r'(^Successfully built |sha256:)([0-9a-f]+)$',
                              chunk['stream'])
            if match:
                image_id = match.group(2)
    if not image_id:
        message = f"Unknown Error while building Dockerfile for pyfixm. " \
                  f"Build did not return an image ID."
        raise DockerBuildError(message)

    image: Image = docker_client.images.get(image_id)
    return image


def extract_files(docker_client: DockerClient, image: Image):

    container: Container = docker_client.containers.create(image)

    # Get archive tar bytes from the container as a sequence of bytes
    package_tar_byte_gen: Generator[bytes, None, None]
    # noinspection PyTypeChecker
    package_tar_byte_gen, _ = container.get_archive("/pyfixm/", chunk_size=None)

    # Concat all the chunks together
    package_tar_bytes: bytes
    package_tar_bytes = b"".join(package_tar_byte_gen)

    # Create a tarfile from the tar bytes
    tar_file_object = io.BytesIO(package_tar_bytes)
    package_tar = tarfile.open(fileobj=tar_file_object)

    # Extract the files from the tarfile to the disk
    for tar_file_info in package_tar.getmembers():
        # Ignore directories
        if not tar_file_info.isfile():
            continue

        # Directory that will contain the output files
        pyfixm_output_path = Path('pyfixm/')
        pyfixm_output_path.mkdir(parents=True, exist_ok=True)

        # Filename (without outer directory)
        tar_file_info.name = Path(tar_file_info.name).name

        # Extract
        package_tar.extract(tar_file_info, pyfixm_output_path)


class DockerBuildError(RuntimeError):
    def __init__(self, message):
        self.message = message


if __name__ == '__main__':
    main()
