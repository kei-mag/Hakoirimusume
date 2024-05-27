package net.keimag.hakoirimusume;

import io.micrometer.common.util.StringUtils;
import org.slf4j.Logger;
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

    public Authorizer(HakoirimusumeProperties.AikotobaProperties aikotobaProperties) {
        this.aikotobaProperties = aikotobaProperties;
    }

    public String generateNewAikotoba(String generationUser) {
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
            log.debug("Aikotoba: {}", this.aikotoba);
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
        if (StringUtils.isBlank(aikotoba) || StringUtils.isBlank(generationUser)) {
            deleteAikotoba();
        }
        if (!Objects.isNull(expirationPeriod) && !expirationPeriod.after(Calendar.getInstance()) && !Objects.isNull(generationUser)) {
            /* do nothing (still valid) */
        } else {
            deleteAikotoba();
        }
        log.debug("aikotoba: {}, generationUser: {}, expirationPeriod: {}", aikotoba, generationUser, expirationPeriod);
    }

    private void deleteAikotoba() {
        aikotoba = null;
        generationUser = null;
        expirationPeriod = null;
        log.debug("Aikotoba was deleted.");
    }
}
