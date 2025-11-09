import hashlib
import json
import uuid
from datetime import datetime

from .Status import Status


class License(object):
    __PREFIX = "----license-----"

    def __init__(self, mac_address: str, expiration_date: datetime):
        self.__mac_address: str = mac_address
        self.__password: str = self.__hash(self.__PREFIX + mac_address)
        self.__expiration_date: datetime = expiration_date

    def name(self) -> str:
        mac_address = self.__mac_address.replace(":", "")
        expiration_date = self.__expiration_date.strftime("%Y%m%d")
        return f"license-{mac_address}-{expiration_date}"

    def text(self):
        license_dict = {
            "mac_address": self.__mac_address,
            "expiration_date": self.__expiration_date.strftime("%Y-%m-%d"),
            "password": self.__password,
        }
        return json.dumps(license_dict)

    def status(self) -> Status:
        if self.__is_expired():
            return Status.EXPIRED
        elif self.__is_illegal():
            return Status.ILLEGAL
        else:
            return Status.VALID

    def __is_expired(self) -> bool:
        now = datetime.now()
        return now > self.__expiration_date

    def __is_illegal(self) -> bool:
        mac_address = self.__get_mac_address()
        password = self.__hash(self.__PREFIX + mac_address)
        return password != self.__password

    def __get_mac_address(self) -> str:
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join([mac[i: i + 2] for i in range(0, 11, 2)])

    def __hash(self, message: str) -> str:
        sha256 = hashlib.sha256()
        sha256.update(message.encode('utf-8'))
        return sha256.hexdigest()

    def __str__(self) -> str:
        return self.text()

    def __repr__(self):
        return self.text()
