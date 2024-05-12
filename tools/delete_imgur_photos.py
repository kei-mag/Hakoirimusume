import sys
from pathlib import Path

import requests

script_name = Path(__file__).name


def delete_from_imgur(client_id: str, deletehash: str) -> str:
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
    header = {"Authorization": f"Client-ID {client_id}"}
    response = requests.delete(f"https://api.imgur.com/3/image/{deletehash}", headers=header)
    return response.text


help_text = f"""Delete image or video file uploaded to imgur.com
If you want to delete every images uploaded by Hakoirimusume, just run `python {script_name}`.

Usage: python {script_name} [options] <deletehash1> <deletehash2> ...
                        OR
       python {script_name} [options] [--file <file-path>]

Arguments:
    deletehash                      Deletehash of the target image or video file
    --file <file-path>              File path containing deletehashes, if not provided, "../sensor-data.csv" is used

Options:
    -i, --client-id <client id>     Imgur Application's Client ID
    -c, --config <config.yml>       Hakoirimusume config file path, absolute path or relative path from this file (default: "../config.yml")
    -h, --help                      Show this help message and exit
"""
if __name__ == "__main__":
    args = " ".join(sys.argv[1:])
    if "-h" in args or "--help" in args:
        print(help_text)
        sys.exit(0)
