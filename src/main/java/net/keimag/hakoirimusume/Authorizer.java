package net.keimag.hakoirimusume;

import io.micrometer.common.util.StringUtils;
import org.slf4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Calendar;
import java.util.Objects;
import java.util.Random;

@Service
public class Authorizer {
    private static final Logger log = org.slf4j.LoggerFactory.getLogger(Authorizer.class);
    private final Random rand = new Random();
    private final HakoirimusumeProperties.AikotobaProperties aikotobaProperties;
    private String aikotoba = null;
    private String generationUser = null;
    private Calendar expirationPeriod = null;

    @Autowired
    public Authorizer(HakoirimusumeProperties hakoirimusumeProperties) {
        this.aikotobaProperties = hakoirimusumeProperties.getAikotoba();
    }

    public String generateNewAikotoba(String generationUser) {
        log.info("Seeds: {}", aikotobaProperties.getSeeds());
        invalidateAikotoba();
        if (!StringUtils.isBlank(this.generationUser) && !this.generationUser.equals(generationUser)) {
            /* User cannot generate new aikotoba while the aikotoba another user generated is valid. */
            return null;
        } else {
            this.aikotoba = "";
            aikotobaProperties.getSeeds().forEach(seed -> {
                int index = rand.nextInt(seed.size());
                this.aikotoba += seed.get(index);
            });
            this.expirationPeriod = Calendar.getInstance();
            this.expirationPeriod.add(Calendar.SECOND, aikotobaProperties.getTimeoutSec());
            this.generationUser = generationUser;
            log.debug("Aikotoba: {}, User: {}, Expiration: {}, Now: {}", this.aikotoba, this.generationUser, this.expirationPeriod.getTime(), Calendar.getInstance().getTime());
            return this.aikotoba;
        }
    }

    public boolean authorize(String aikotoba) {
        invalidateAikotoba();
        boolean isSucceed = false;
        if (aikotoba.equals(this.aikotoba)) {
            isSucceed = true;
        }else {
            isSucceed = false;
        }
        log.debug("CurrentAikotoba: {}, EnteredAikotoba: {}, isSucceed: {}", this.aikotoba, aikotoba, isSucceed);
        deleteAikotoba();
        return isSucceed;
    }

    @SuppressWarnings("StatementWithEmptyBody")
    private void invalidateAikotoba() {
        log.debug("Invalidating Aikotoba");
        if (StringUtils.isBlank(aikotoba) || StringUtils.isBlank(generationUser)) {
            deleteAikotoba();
        }
        if (!Objects.isNull(expirationPeriod) && Calendar.getInstance().before(this.expirationPeriod) && !Objects.isNull(generationUser)) {
            /* do nothing (still valid) */
        } else {
            deleteAikotoba();
        }
    }

    private void deleteAikotoba() {
        aikotoba = null;
        generationUser = null;
        expirationPeriod = null;
        log.debug("Aikotoba was deleted.");
    }
}
