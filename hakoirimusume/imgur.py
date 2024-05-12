"""Upload & delete image files & video files to (from) imgur.com

This scripts supports Imgur API version 3.

This script works with Python 3.10 or later.
If you are running this script in Python 3.9 or earlier,
please uncomment line 10 or rewrite the type annotations in the corresponding format.
"""

from __future__ import annotations  # For Python 3.8 - 3.9

import json
from io import BufferedReader
from typing import Literal

import requests

# Imgur API version 3
# Upload: https://api.imgur.com/3/upload
# Get: https://api.imgur.com/3/image/{id}
IMGUR_API_URI = r'https://api.imgur.com/3'


def upload_as_anonymous(
    client_id: str,
    file: bytes | BufferedReader,
    type: Literal["image", "video"] = "image",
    name: str | None = None,
    verbose: bool = False,
) -> tuple[str, str] | str:
    """Upload image or video files anonymously to imgur.com

    Parameters
    ----------
    client_id : str
        Imgur Application's Client ID
    file : bytes | BufferedReader
        Files to be uploaded.
    type : Literal['image', 'video'], optional
        Specify file type as 'image' file or 'video' file, by default 'image'
    name : str | None, optional
        File name, by default None

    Returns
    -------
    tuple[str, str] | str
        If the file is successfully uploaded, tuple with a link to the file and a deletehash is returned.
        If it fails, the contents of the response body are returned as text.
    """
    header = {
        "Authorization": f"Client-ID {client_id}"
    }
    payload = {
        "type": "file",
        "title": "Rabbit’s House Report Image － today",
        "description": 'This image is posted by LINE BOT "箱入り娘" automatically.',
    }
    files = [(type, file)]
    if name is not None:
        payload["name"] = name
    response = requests.post(IMGUR_API_URI + "/image", headers=header, data=payload, files=files)
    if verbose:
        print("Request:")
        print("    Header:", header)
        print("    Payload:", payload)
        print("    Files:", files)
    if response.status_code == 200:
        response_json = json.JSONDecoder().decode(response.text)
        return response_json["data"]["link"], response_json["data"]["deletehash"]
    else:
        return response.text


def delete_from_imgur(client_id: str, deletehash: str) -> str | Literal[True]:
    """Delete image or video file uploaded to imgur.com

    Parameters
    ----------
    client_id : str
        Imgur Application's Client ID
    deletehash : str
        Target file's deletehash provided by `upload_as_anonymous` function.

    Returns
    -------
    str | Literal[True]
        Return `True` if the Imgur server returns status code 200.
        If it fails, the contents of the response body are returned in text.
    """
    header = {
        "Authorization": f"Client-ID {client_id}"
    }
    response = requests.delete(
        IMGUR_API_URI+f'/image/{deletehash}', headers=header)
    if response.status_code == 200:
        return True
    else:
        return response.text
