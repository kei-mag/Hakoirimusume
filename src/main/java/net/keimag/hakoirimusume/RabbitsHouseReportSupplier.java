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
import java.util.Date;
import java.util.function.Supplier;

public class RabbitsHouseReportSupplier implements Supplier<FlexMessage> {
    private static final Logger log = LoggerFactory.getLogger(RabbitsHouseReportSupplier.class);

    private final String templateJson;
    private final Calendar c = Calendar.getInstance();
    private final SimpleDateFormat uiDateFormat = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
    private final SimpleDateFormat numericDateFormat = new SimpleDateFormat("yyyyMMddHHmmss");
    private final DecimalFormat df = new DecimalFormat("0.0");

    public RabbitsHouseReportSupplier(String templateJsonPath) throws IOException {
        this.templateJson = Files.readString(Path.of(templateJsonPath));
    }

    private String getMessage(double temp, double hum, double pressure) {
        if (temp == 0.0 && hum == 0.0 && pressure == 0.0) {
            return "今何度？部屋に来て確認してほしい！🌡️";
        } else {
            if (temp >= 27.0) {
                return "今すぐ助けて！熱中症になっちゃう😵";
            } else if (temp >= 26.0) {
                if (hum > 60.0) {
                    return "暑い🥵限界！今すぐエアコン点けて！";
                } else {
                    return "暑すぎてもう限界！エアコン点けて！";
                }
            } else if (temp > 25.0) {
                if (hum > 60.0) {
                    return "暑いしジメジメしすぎ！エアコンオン！";
                } else if (hum >= 40.0) {
                    return "外出するならエアコン点けていって！";
                } else {
                    return "脱水症状を気にかけてほしいな。";
                }
            } else if (temp > 24.0) {
                if (hum >= 70.0) {
                    return "ジメジメしすぎ！今すぐ除湿して！";
                } else if (hum > 60.0) {
                    return "ジメジメしてるから窓開けてほしいな";
                } else if (hum >= 40.0) {
                    return "ちょっと暑いけど頑張るよ。";
                } else {
                    return "脱水症状を気にかけてほしいな。";
                }
            } else if (temp >= 17.0) {
                if (hum >= 70.0) {
                    return "ジメジメしすぎてる！今すぐ除湿して！";
                } else if (hum > 60.0) {
                    return "ジメジメしてるから除湿してほしいな";
                } else if (hum >= 35.0) {
                    return "今のところは快適だよ！😁👌";
                } else {
                    return "乾燥しすぎだから加湿器つけてほしいな";
                }
            } else {
                return "寝るときにヒーター点けてほしいな🙏";
            }
        }
    }



    private String getReportJson() throws IOException, InterruptedException {
        String reportJson = templateJson;
        String temp = "---", humidity = "---", pressure = "---";
//        if (bme280Data != null) {
//            temp = df.format(bme280Data.temperature);
//            humidity = df.format(bme280Data.humidity);
//            pressure = df.format(bme280Data.pressure / 100);  // 1 Pa = 0.01 hPa
//            if (bme280Data.temperature >= 27.0 || (bme280Data.temperature >= 26.0 && bme280Data.humidity > 60)) {
//                reportJson = reportJson.replace("#FFFFFF", "#DC3545");  // Red frame border
//            }
//        }
        String imageUri = null;
        Date currentTime = c.getTime();
        reportJson = reportJson.replace("{{CurrentTime}}", uiDateFormat.format(currentTime));
        reportJson = reportJson.replace("{{Temperature}}", temp);
        reportJson = reportJson.replace("{{Humidity}}", humidity);
        reportJson = reportJson.replace("{{Pressure}}", pressure);
//        reportJson = reportJson.replace("{{Message}}");
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
        try {
            return new FlexMessageBuilder().build("Rabbit's House Report", getReportJson());
        } catch (IOException | InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    public FlexMessage alert() throws IOException, InterruptedException {
        String contents = getReportJson();
        contents = contents.replace("Rabbit's House Report", "Rabbit's House Alert!");
        contents = contents.replace("#1DB446", "#DC3545");
        contents = contents.replace("#FFFFFF", "#DC3545");  // Red frame border
        return new FlexMessageBuilder().build("Rabbit's House Alert!", contents);
    }
}
