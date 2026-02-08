"""Upload image to s3 (compatible) object storage."""
from logging import getLogger

import boto3
from botocore.exceptions import ClientError
from typing import Optional, Any, BinaryIO, Literal
from os import PathLike
from datetime import datetime
from pathlib import Path
import io
from urllib.parse import urlparse

logger = getLogger(__name__)

def upload_file(
    file: str | PathLike | BinaryIO | bytes,
    bucket: str,
    object_name=None,
    ExtraArgs: Optional[dict[str, Any]] = None,
    endpoint_url: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region_name: Optional[str] = None,
    url_format: Literal["path", "virtualhost"] = "path"
):
    """Upload a file to an S3 bucket

    Parameters
    ----------
    file : filepath, file-like object or PNG Image bytes
        File to upload
    bucket : str
        Bucket to upload to
    object_name: str, optional
        S3 object name. If not specified then file-name or current timestamp is used
    ExtraArgs : dict, optional
        See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html#the-extraargs-parameter
    endpoint_url : str, optional
        Endpoint URL of S3 (compatible) storage. Defaults to AWS
    aws_access_key_id : str, optional
        AWS access key ID. Credentials were searched automatically if not specified.
        (See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#guide-configuration)
    aws_secret_access_key : str, optional
        AWS secret access key. Credentials were searched automatically if not specified.
        (See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#guide-configuration)
    region_name : str, optional
        AWS region name. Credentials were searched automatically if not specified.
        (See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#guide-configuration)
    url_format : "path" or "virtualhost", optional
        The format of the returned URL. Defaults to "path".
        - "path": Returns URL as `http(s)://host/bucket/key`.
            Recommended for local environments (MinIO, SeaweedFS), IP-based endpoints, or private networks.
        - "virtualhost": Returns URL as `http(s)://bucket.host/key`.
            Recommended for S3-compatible storage with DNS configured (e.g., Garage Web hosting).

    Returns
    -------
    str | False: Image URL if file was uploaded, else False
    """
    is_filepath = isinstance(file, str) or isinstance(file, PathLike)

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        if is_filepath:
            object_name = Path(file).name  # type: ignore
        else:
            if filename:=getattr(file, "name"):
                object_name = Path(filename).name
            else:
                if isinstance(file, bytes):
                    object_name = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S%z.png")
                else:
                    object_name = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S%z")

    # Upload the file
    extra_config = {
        k: v
        for k, v in {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "region_name": region_name,
            "endpoint_url": endpoint_url,
        }.items()
        if v is not None
    }
    s3_client = boto3.client("s3", **extra_config)
    try:
        if is_filepath:
            if ExtraArgs:
                response = s3_client.upload_file(file, bucket, object_name, ExtraArgs=ExtraArgs)
            else:
                response = s3_client.upload_file(file, bucket, object_name)
        else:
            if isinstance(file, bytes):
                file = io.BytesIO(file)
            if ExtraArgs:
                response = s3_client.upload_fileobj(file, bucket, object_name, ExtraArgs=ExtraArgs)
            else:
                response = s3_client.upload_fileobj(file, bucket, object_name)
        logger.info(response)
    except ClientError as e:
        logger.error(e)
        return False
    # Generate Image URL
    if "s3.amazonaws.com" in s3_client.meta.endpoint_url:
        # AWS S3
        return f"https://{bucket}.s3.{s3_client.meta.region_name}.amazonaws.com/{object_name}"
    else:
        # S3 compatible storage (GarageHQ, SeaweedFS, etc.)
        if url_format == "virtualhost":
            # Virtual host format
            parsed = urlparse(s3_client.meta.endpoint_url)
            return f"{parsed.scheme}://{bucket}.{parsed.netloc}/{object_name}"
        else:
            # Path format
            return f"{s3_client.meta.endpoint_url.rstrip('/')}/{bucket}/{object_name}"
