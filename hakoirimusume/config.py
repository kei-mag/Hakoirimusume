import os
import re

import hakoirimusume.enhanced_yaml as enhanced_yaml


class Config:
    def __init__(self, file: str = "./config.yml") -> None:
        self.__config_dict = enhanced_yaml.safe_load(open(file, "r", encoding="UTF-8"))
        self.__config_file = file
        # print(self.__config_dict)

    def get(self, key: str, default=None):
        try:
            value = enhanced_yaml.get(self.__config_dict, key)
            # print("value: ", value)
            if isinstance(value, str):
                # print("isinstance(value, str):", value)
                match_env = re.match(r"\$\{(.*)\}", value)
                if match_env:
                    # print("match_env:", match_env.group(1))
                    return os.environ.get(match_env.group(1), default)
                else:
                    return value
            return value
        except FileNotFoundError:
            return default

    # @singledispatchmethod
    # def set(self, key: str, value):
    #     keys = key.split(".")
    #     element = self.__config_dict
    #     for k in keys[:-1]:
    #         print(f"----- (k={k}) -----")
    #         print(element, "↓", sep="\n")
    #         element = element[k]
    #         print(element)
    #     print("End of for loop.", "element:", element)
    #     element = value
    #     self._save()

    # @set.register
    # def set_dict(self, key_value: dict):
    #     for key, value in key_value.items():
    #         keys = key.split(".")
    #         element = self.__config_dict
    #         for k in keys[:-1]:
    #             element = element[k]
    #         element = value
    #     self._save()

    # def _save(self):
    #     with open(self.__config_file, "w", encoding="UTF-8") as stream:
    #         self.yaml.dump(self.__config_dict, stream)


config = Config()  # Use this normally.
