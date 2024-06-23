package net.keimag.hakoirimusume;

import org.junit.jupiter.api.Test;
import org.slf4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ContextConfiguration;

@SpringBootTest
@ContextConfiguration(classes = HakoirimusumeApplication.class)
class HakoirimusumePropertiesTests {
    static final Logger log = org.slf4j.LoggerFactory.getLogger(HakoirimusumePropertiesTests.class);

    @Autowired
    HakoirimusumeProperties properties;

    @Test
    void loadTest() {
        log.info("loadTest");
        var alert = properties.getAlert();
        var triggerLimit = alert.getTriggerLimit();
        log.info("hakoirimusume.alert.trigger-limit.interval: {}", triggerLimit.getInterval());
        log.info("hakoirimusume.alert.daily-limit: {}", triggerLimit.getDailyLimit());
        var condition = alert.getCondition();
        log.info("hakoirimusume.alert.condition.temperature: {}", condition.getTemperature());
        log.info("hakoirimusume.alert.condition.humidity: {}", condition.getHumidity());
        var action = alert.getAction();
        log.info("hakoirimusume.alert.action.type: {}", action.getType());
        log.info("hakoirimusume.alert.action.target: {}", action.getTarget());
        log.info("hakoirimusume.alert.action.header: {}", action.getHeader());
        log.info("hakoirimusume.alert.action.body: {}", action.getBody());
        log.info("hakoirimusume.alert.action.success-message: {}", action.getSuccessMessage());
        log.info("hakoirimusume.alert.action.failure-message: {}", action.getFailureMessage());
        var aikotoba = properties.getAikotoba();
        log.info("hakoirimusume.aikotoba.seeds: {}", aikotoba.getSeeds());
        log.info("hakoirimusume.aikotoba.timeout-sec: {}", aikotoba.getTimeoutSec());
        var info = properties.getInfo();
        log.info("hakoirimusume.info.show-private-ip: {}", info.isShowPrivateIp());
    }
}
