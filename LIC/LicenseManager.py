import json
from pathlib import Path
from datetime import datetime, timedelta

from .Cryptograph import Cryptograph
from .License import License
from .Status import Status


class LicenseManager(object):
    __SECRET_KEY: str = "license"

    def __init__(self, secret_key: str):
        self.SECRET_KEY = secret_key

    @classmethod
    def generate_license(cls, mac_address: str, duration: int, license_dir: Path) -> Path:
        license = License(mac_address, datetime.today() + timedelta(days=duration))
        cryptograph = Cryptograph(cls.__SECRET_KEY)
        ciphertext = cryptograph.encrypt(license.text())
        license_file = license_dir / (license.name() + ".lic")
        with open(license_file, mode="w") as f:
            f.write(ciphertext)
        return license_file

    @classmethod
    def check_license(cls, license_file: Path) -> Status:
        with open(license_file, mode="r") as f:
            ciphertext = f.readline()
        cryptograph = Cryptograph(cls.__SECRET_KEY)
        plaintext = cryptograph.decrypt(ciphertext)
        license_dict = json.loads(plaintext)
        mac_address = license_dict["mac_address"]
        expiration_date = datetime.strptime(license_dict["expiration_date"], "%Y-%m-%d")
        license = License(mac_address, expiration_date)
        return license.status()
