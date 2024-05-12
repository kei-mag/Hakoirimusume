from datetime import datetime, timedelta
from random import Random

from hakoirimusume.config import ConfigurationError, config


class Authorizer:
    def __init__(self) -> None:
        self.random = Random()
        sheeds = config.get("hakoirimusume.aikotoba.sheeds")
        timeout = config.get("hakoirimusume.aikotoba.timeout")
        if sheeds is None or not isinstance(timeout, int):
            raise ConfigurationError(
                "Seeds or Valid period of Aikotoba is not configured correctly in config.yml."
                "Plsease check hakoitimusume.aikotoba"
            )
        else:
            self.sheeds = sheeds
            self.timeout_sec = timeout
        self._reset_aikotoba()

    def create_new_aikotoba(self, request_user: str):
        self.aikotoba = ""
        if self.expired_time is not None and self.expired_time >= datetime.now() and request_user != self.request_user:
            # print(f"Current Request user is {request_user}, but {self.request_user} is requesting. Block creation.")
            return False
        for words in self.sheeds:
            self.random.shuffle(words)  # type: ignore
            self.aikotoba += words[0]
        self.expired_time = datetime.now() + timedelta(seconds=self.timeout_sec)
        self.request_user = request_user
        # print(self.aikotoba)
        return self.aikotoba

    def authorize(self, aikotoba: str):
        if not self.aikotoba or not self.expired_time or not self.request_user:
            # print("Aikotoba is not created.")
            result = False
        else:
            if datetime.now() > self.expired_time:
                # print("Expired Aikotoba.")
                result = False
            else:
                result = self.aikotoba == aikotoba
        self._reset_aikotoba()
        return result

    def _reset_aikotoba(self):
        self.aikotoba = None
        self.expired_time = None
        self.request_user = None
