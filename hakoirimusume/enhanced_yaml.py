from copy import deepcopy
from typing import Sequence

import yaml


class YamlUtils:

    def yaml_dict_to_text(self, yaml_dict, parent_key, yaml_text):
        return_value = yaml_text.split("\n")
        for key, value in yaml_dict.items():
            key_string = key
            if parent_key != "":
                key_string = parent_key + "." + key_string
            if isinstance(value, dict):
                return_value.append(self.yaml_dict_to_text(value, key_string, yaml_text))
            else:
                return_value.append("{0}: {1}".format(key_string, value))
        return "\n".join(return_value).replace("None", "null")

    @staticmethod
    def convert_to_dict(source_string, split_symbol=".", value=None):
        # return_value = value
        # print("value:", value)
        return_value = dict(yaml.safe_load(f"value: {value}"))["value"] if value is not None else value
        # if value is not None and re.match(r"\s*\[.*\]\s*", value):
        #     d = dict(yaml.safe_load(f"value: {value}"))
        #     print("d:", d)
        #     return_value = d["value"]
        # else:
        #     return_value = value
        elements = source_string.split(split_symbol)
        for element in reversed(elements):
            if element:
                return_value = {element: return_value}
        return return_value

    def dict_of_dicts_merge(self, x, y):
        # print("x:", x)
        # print("y:", y)
        z = {}
        try:
            overlapping_keys = x.keys() & y.keys()
            for key in overlapping_keys:
                z[key] = self.dict_of_dicts_merge(x[key], y[key])
            for key in x.keys() - overlapping_keys:
                z[key] = deepcopy(x[key])
            for key in y.keys() - overlapping_keys:
                z[key] = deepcopy(y[key])
        except Exception as e:
            raise self.MergeDictsError("Error merging dicts:", x, y, str(e))
        return z

    def text_to_yaml_dict(self, yaml_text):
        return_value = {}
        yaml_list = yaml_text.split("\n")
        for line in yaml_list:
            line_items = line.split(":")
            if len(line_items) >= 2:
                line_key = line_items[0]
                line_value = line_items[1].lstrip()
                line_dict = self.convert_to_dict(line_key, ".", line_value)
                return_value = self.dict_of_dicts_merge(return_value, line_dict)
        return return_value

    class MergeDictsError(Exception):
        pass


def get(yaml_dict, key: str):
    keys = key.split(".")
    element = yaml_dict
    for k in keys:
        # print(f"k={k}")
        if isinstance(element, Sequence) and k.isdigit():
            element = element[int(k)]
        else:
            element = element[k]  # type: ignore
    return element


def safe_load(stream):
    yaml_dict = yaml.safe_load(stream)
    yaml_utils = YamlUtils()
    processed_yaml_text = yaml_utils.yaml_dict_to_text(
        yaml_dict,
        "",
        "",
    )
    # print("processed_yaml_text:", processed_yaml_text)
    processed_yaml_dict = yaml_utils.text_to_yaml_dict(processed_yaml_text)
    return processed_yaml_dict
