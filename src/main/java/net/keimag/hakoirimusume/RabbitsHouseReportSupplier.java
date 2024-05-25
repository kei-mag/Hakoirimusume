package net.keimag.hakoirimusume;

import com.linecorp.bot.messaging.model.FlexMessage;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.text.DecimalFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.function.Supplier;

public class RabbitsHouseReportSupplier implements Supplier<FlexMessage> {
    private static final Logger log = LoggerFactory.getLogger(RabbitsHouseReportSupplier.class);

    private final String templateJson;
    private final Calendar c = Calendar.getInstance();
    private final SimpleDateFormat cf = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
    private final BME280 bme280;
    private final DecimalFormat df = new DecimalFormat("0.0");

    public RabbitsHouseReportSupplier(String templateJsonPath, BME280 bme280) throws IOException{
        this.templateJson = Files.readString(Path.of(templateJsonPath));
        this.bme280 = bme280;
    }

    private String getMessage(BME280.BME280Data d) {
        if (d != null) {
            if (d.temperature >= 27.0) {
                return "今すぐ助けて！熱中症になっちゃう😵";
            } else if (d.temperature >= 26.0) {
                if (d.humidity > 60.0) {
                    return "暑い🥵限界！今すぐエアコン点けて！";
                } else {
                    return "暑すぎてもう限界！エアコン点けて！";
                }
            } else if (d.temperature > 25.0) {
                if (d.humidity > 60.0) {
                    return "暑いしジメジメしすぎ！エアコンオン！";
                } else if (40.0 <= d.humidity) {
                    return "外出するならエアコン点けていって！";
                } else {
                    return "脱水症状を気にかけてほしいな。";
                }
            } else if (d.temperature > 24.0) {
                if (d.humidity >= 70.0) {
                    return "ジメジメしすぎ！今すぐ除湿して！";
                } else if (d.humidity > 60.0) {
                    return "ジメジメしてるから窓開けてほしいな";
                } else if (40.0 <= d.humidity) {
                    return "ちょっと暑いけど頑張るよ。";
                } else {
                    return "脱水症状を気にかけてほしいな。";
                }
            } else if (17.0 <= d.temperature) {
                if (d.humidity >= 70.0) {
                    return "ジメジメしすぎてる！今すぐ除湿して！";
                } else if (d.humidity > 60.0) {
                    return "ジメジメしてるから除湿してほしいな";
                } else if (35.0 <= d.humidity) {
                    return "今のところは快適だよ！😁👌";
                } else {
                    return "乾燥しすぎだから加湿器つけてほしいな";
                }
            } else if (d.temperature > 13.0) {
                return "体調変化を気にかけてほしいな。";
            } else {
                return "寝るときにヒーター点けてほしいな🙏";
            }
        } else {
            return "今何度？ 部屋に来て確認してほしい！";
        }
    }

    private String getReportJson() {
        String reportJson = templateJson;
        String imageUri = null;
        String currentTime = cf.format(c.getTime());
        BME280.BME280Data bme280Data = this.bme280.getMeasurements();
        String temp = "---", humidity = "---", pressure = "---";
        if (bme280Data != null) {
            temp = df.format(bme280Data.temperature);
            humidity = df.format(bme280Data.humidity);
            pressure = df.format(bme280Data.pressure / 100);  // 1 Pa = 0.01 hPa
            if (bme280Data.temperature >= 27.0 || (bme280Data.temperature >= 26.0 && bme280Data.humidity > 60)) {
                reportJson = reportJson.replace("#FFFFFF", "#DC3545");  // Red frame border
            }
        }
        reportJson = reportJson.replace("{{CurrentTime}}", currentTime);
        reportJson = reportJson.replace("{{Temperature}}", temp);
        reportJson = reportJson.replace("{{Humidity}}", humidity);
        reportJson = reportJson.replace("{{Pressure}}", pressure);
        reportJson = reportJson.replace("{{Message}}", getMessage(bme280Data));
        if (imageUri != null) {
            reportJson = reportJson.replace("https://i.imgur.com/Z5GS685.jpeg", imageUri);
        } else {
            reportJson = reportJson.replace(",\n" +
                    "    \"action\": {\n" +
                    "      \"type\": \"uri\",\n" +
                    "      \"uri\": \"https://i.imgur.com/Z5GS685.jpeg\",\n" +
                    "      \"label\": \"View image at Imgur\"\n" +
                    "    }", "");
        }
        return reportJson;
    }

    public FlexMessage get() {
        return new FlexMessageBuilder().build("Rabbit's House Report", getReportJson());
    }

    public FlexMessage alert() {
        String contents = getReportJson();
        contents = contents.replace("Rabbit's House Report", "Rabbit's House Alert!");
        contents = contents.replace("#1DB446", "#DC3545");
        contents = contents.replace("#FFFFFF", "#DC3545");  // Red frame border
        return new FlexMessageBuilder().build("Rabbit's House Alert!", contents);
    }
}
