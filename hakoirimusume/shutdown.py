import os
import sys

from hakoirimusume.config import config


def shutdown():
    config.get("hakoirimusume.remote-shutdown.enable")
    os.system(config.get("hakoitimusume.remote-shutdown.command", "shutdown -h -t 15"))  # type: ignore
    return True
