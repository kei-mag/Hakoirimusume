import json
from datetime import datetime

from linebot.v3.messaging import FlexContainer, FlexMessage

# from . import bme280


class ReportCreater:

    def __init__(self) -> None:
        with open("hakoirimusume/templates/report_template.json", "r", encoding="utf-8") as f:
            self.report_template = json.load(f)
        # self.bme280 = bme280.BME280(1, 0x76)

    def get_report(self) -> FlexContainer:
        report_dict = self.report_template.copy()
        image_url = None
        current_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        temp_hum_pressure = None  # self.bme280.read_data()
        message = self.get_message(temp_hum_pressure)
        if temp_hum_pressure is None:
            temperature = humidity = pressure = "---"
        else:
            temperature, humidity, pressure = temp_hum_pressure
            if temperature >= 27.0 or (temperature >= 26.0 and humidity > 60):
                report_dict["body"]["borderColor"] = "#DC3545"
        if image_url:
            report_dict["hero"]["url"] = image_url  # Replace image
        else:
            del report_dict["hero"]["action"]  # Remove image tap action
        report_dict["body"]["contents"][1]["text"] = current_time
        report_dict["body"]["contents"][3]["contents"][1]["text"] = message
        report_dict["body"]["contents"][4]["contents"][0]["contents"][1]["text"] = temperature
        report_dict["body"]["contents"][4]["contents"][1]["contents"][1]["text"] = humidity
        report_dict["body"]["contents"][4]["contents"][2]["contents"][1]["text"] = pressure
        return FlexMessage(altText="Rabbit's House Report", contents=FlexContainer.from_dict(report_dict))

    def get_message(self, temp_hum_pressure: tuple[float, float, float] | None = None):
        if temp_hum_pressure is not None:
            temp, hum, pressure = temp_hum_pressure
            if temp >= 27.0:
                return "今すぐ助けて！熱中症になっちゃう😵"
            elif temp >= 26.0:
                if hum > 60.0:
                    return "暑い🥵限界！今すぐエアコン点けて！"
                else:
                    return "暑すぎてもう限界！エアコン点けて！"
            elif temp > 25.0:
                if hum > 60.0:
                    return "暑いしジメジメしすぎ！エアコンオン！"
                elif 40.0 <= hum:
                    return "外出するならエアコン点けていって！"
                else:
                    return "脱水症状を気にかけてほしいな。"
            elif temp > 24.0:
                if hum >= 70.0:
                    return "ジメジメしすぎ！今すぐ除湿して！"
                elif hum > 60.0:
                    return "ジメジメしてるから窓開けてほしいな"
                elif 40.0 <= hum:
                    return "ちょっと暑いけど頑張るよ。"
                else:
                    return "脱水症状を気にかけてほしいな。"
            elif 17.0 <= temp:
                if hum >= 70.0:
                    return "ジメジメしすぎてる！今すぐ除湿して！"
                elif hum > 60.0:
                    return "ジメジメしてるから除湿してほしいな"
                elif 35.0 <= hum:
                    return "今のところは快適だよ！😁👌"
                else:
                    return "乾燥しすぎだから加湿器つけてほしいな"
            elif temp > 13.0:
                return "体調変化を気にかけてほしいな。"
            else:
                return "寝るときにヒーター点けてほしいな🙏"
        else:
            return "今何度？部屋に来て確認してほしい！🌡️"
