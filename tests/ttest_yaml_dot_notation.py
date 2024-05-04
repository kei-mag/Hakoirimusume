import re
from copy import deepcopy
from typing import Sequence

import yaml

my_yaml = """
os.environ.path: ${PATH}

test.0.key: value

# Flask server
server.port: 8080

# LINE Messaging API
line.bot:
  channel-token: ${LINE_CHANNEL_ACCESS_TOKEN}
  channel-secret: ${LINE_CHANNEL_SECRET}
  handler.path: /callback

service.scalingPolicy.capacity:
    min: 1
    max: 50
    
hakoirimusume:
  alert:
    condition:  # [!This value can be changed via LINE!]
      temperature: 26.5  # °C  float
      humidity: 60  # %  float
      pressure: null  # hPa  float
    interval: 3  # hour
    restrict:
      times-of-day: 5
      disable-message-threshold: 180  # messages / month
    action:
      type: POST  # GET | POST | COMMAND | null
      # The following placeholders are available in 'target', 'header', 'body'.
      # {{IMAGE_URL}} : Imgur URL of image (will be replaced with empty string when camera image is not available)
      # {{TEMP}} : Current temperature (e.g., 25.0)
      # {{HUMID}} : Current humidity (e.g., 50.0)
      # {{PRESSURE}} : Current pressure (e.g., 1013.0)
      # {{DATE}} : yyyymmdd string of current date (e.g., 20240425)
      # {{TIME}} : HHMMSS string of current local time (e.g., 113911)
      target: null  # URL (type is GET or POST) | shell command (type is COMMAND) | null
      header: null  # String | null, ignored if type is not POST
      body: null  # String | null, ignored if type is not POST
      success-message: "冷房を点けたよ！"  # String | null
      failure-message: "冷房を点けるのに失敗しちゃった、部屋に来て点けて！"  # String | null
  # Aikotoba configs
  aikotoba:
    timeout: 60  # sec.
    sheeds: 
      - ["お利口で", "かしこくて", "賢くて", "かわいくて", "可愛くて", "キュートで", "げんきで", "元気で", "人見知りで", "優しくて"]
      - ["ご機嫌な", "自立した", "よく食べる", "食欲旺盛な", "天才な", "なんでも食べる？", "長寿な", "長生きな", "甘えん坊な", "癒される"]
      - ["うさぎ", "ウサギ", "Rabbit", "ラビット", "うさちゃん", "うさぎちゃん", "箱入り娘", "耳の長い家族", "ドワーフ", "お姫さま"]
"""


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
        return "\n".join(return_value)

    @staticmethod
    def convert_to_dict(source_string, split_symbol=".", value=None):
        # return_value = value
        print("value:", value)
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
        print("x:", x)
        print("y:", y)
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
            print("Error merging dicts:", x, y, str(e))
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
                if line_key == "hakoirimusume.aikotoba.sheeds":
                    print("line_key:", line_key)
                    print(
                        "line_value:",
                        line_value,
                    )
                    print("line_dict:", line_dict, sep="\n")
                return_value = self.dict_of_dicts_merge(return_value, line_dict)
        return return_value


def get(yamldict, key: str):
    keys = key.split(".")
    element = yamldict
    for k in keys:
        # print(f"k={k}")
        if isinstance(element, Sequence) and k.isdigit():
            element = element[int(k)]
        else:
            element = element[k]  # type: ignore
    return element


def main():
    try:
        yaml_dict = yaml.safe_load(my_yaml)
        print(yaml_dict)
        yaml_utils = YamlUtils()
        processed_yaml_text = yaml_utils.yaml_dict_to_text(
            yaml_dict,
            "",
            "",
        )
        # print("processed_yaml_text:", processed_yaml_text, sep="\n")
        processed_yaml_dict = yaml_utils.text_to_yaml_dict(processed_yaml_text)
        # print("processed_yaml_dict(text_to_yaml_dict):", processed_yaml_dict, sep="\n")
        # print("Min:", processed_yaml_dict["service"]["scalingPolicy"]["capacity"]["min"])
        # print("Max:", processed_yaml_dict["service"]["scalingPolicy"]["capacity"]["max"])
        # print("Test", processed_yaml_dict["hakoirimusume"]["alert"]["action"]["type"])
        # print("Testa", get(processed_yaml_dict, "hakoirimusume.alert.action.type"))
        # print("Test2", processed_yaml_dict["hakoirimusume"]["aikotoba"])
        # print("Test2a", get(processed_yaml_dict, "hakoirimusume.aikotoba.sheeds"))
        data = yaml.dump(processed_yaml_dict, indent=True)
        # print("New yaml:", dict(data), sep="\n")
        print("New yaml:", processed_yaml_dict, sep="\n")
        print(get(processed_yaml_dict, "test.0.key"))
    except yaml.YAMLError as exc:
        print(exc)


main()
