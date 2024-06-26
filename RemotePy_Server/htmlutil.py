"""Utilities about HTML processing"""
import ujson
from ucollections import OrderedDict


def create_error_html(e, loc=None):
    """Provide HTML text where error is described
    
    Args:
        e (Exception): Error or exception object
        loc (str | None): location or function where error occurred,
        " while {loc}" will be put on the bottom of the page if loc is not None.
    
    Returns:
        str: HTML text of error page
    """
    if not loc:
        loc = ""
    else:
        loc = f" while {loc}"
    return f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>RemotePy Server</title>
    </head>
    <body>
        <h1>Initialization Error</h1>
        The following error was occurred during initialization.<br>
        <b>{e}</b><br>
        {loc}
    </body>
    </html>
    """


def parse_codes_json(filename):
    """Parse JSON file and provide HTML text of command list and signal table

    Args:
        filename (str): path to IR command definition file
    
    Returns:
        str: HTML text of Command List block
        dict[str, list[int]]: Dictionary of CommandName and IRSignalData
        
    Raises:
        ValueError: Format of given JSON file is not supported.
    
    Note:
    Acceptable format of JSON file is as follows:
    1. cgir format (created by `cgir rec COMMAND_NAME`)
        ```
        {
            "COMMAND_NAME": [IR_SIGNAL_DATA]
        }
        ```
    2. original format (see also README.md)
        ```
        {
            "COMMAND_NAME": {
                "category": "CATEGORY_NAME",
                "signal": [IR_SIGNAL_DATA],
                "comment": "COMMENT"
            }
        }
        ```
    `COMMAND_NAME` must be unique within a file.
    """
    json_str = open(filename, "r", encoding="UTF-8").read()
    json_dict = ujson.loads(json_str)
    # Fix dictionary order
    command_names = json_dict.keys()
    command_names = [(command, json_str.find(f'"{command}":')) for command in command_names]
    command_names.sort(key=lambda t: t[1])
    fixed_json_dict = OrderedDict()
    for command_name, _ in command_names:
        fixed_json_dict[command_name] = json_dict[command_name]
    del json_str, json_dict
    # Create dict of Command List & Signal Table
    commands_list = OrderedDict({"Others": {}})
    signal_table = {}  # "commandname": [signal list]
    for k, v in fixed_json_dict.items():
        if isinstance(v, list):
            # cgir format
            commands_list["Others"][k] = {"signal": v, "comment": ""}
            signal_table[k] = v
        elif isinstance(v, dict):
            # original format
            category = v.get("category", "Others")
            if not category:
                category = "Others"
            if not v.get("signal"):
                raise ValueError(f"signal data is not found in {k}")
            if category not in commands_list:
                commands_list[category] = OrderedDict()
            commands_list[category][k] = {"signal": v["signal"], "comment": v.get("comment", "")}
            signal_table[k] = v["signal"]
        else:
            raise ValueError(f"unknown format: {k}")
    others = commands_list.pop("Others")
    if others:
        commands_list["Others"] = others
    return _create_command_list_html(commands_list), signal_table


def _create_command_list_html(commands_list):
    """Provide HTML text of Command list block

    Args:
        command_list (dict[str, dict[str, dict[str, Any]]]): Dictionary of `{"CATEGORY_NAME": {"COMMAND_NAME": {"signal": [IR_SIGNAL_DATA], "comment": "COMMENT"}}}`
    
    Return:
        str: HTML text of command list (COMMAND_NAME button and COMMENT is listed by categories.)
    """
    body_html = ""
    for category, commands in commands_list.items():
        if category == "Others" and len(commands_list) <= 1:
            pass
        else:
            body_html += f"<h3>{category}</h3>\n"
        body_html += "<ul>\n"
        for command, data in commands.items():
            body_html += f"<button style=\"font-size:20pt;\" onClick=\"location.href='{command}'\">{command}</button> {data["comment"]}<br><br>\n"
        body_html += "</ul>\n"
    return body_html
