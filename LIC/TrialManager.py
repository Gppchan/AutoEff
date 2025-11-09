import os
from datetime import datetime, timedelta
from pathlib import Path

from .Cryptograph import Cryptograph
from .Status import Status
from .Trial import Trial


class TrialManager(object):
    __SECRET_KEY: str = "-----trial------"

    @classmethod
    def generate_trial(cls, duration: int, trial_dir: Path) -> Path:
        trial = Trial.first(duration)
        cryptograph = Cryptograph(cls.__SECRET_KEY)
        ciphertext = cryptograph.encrypt(trial.dump())
        trial_file = trial_dir / (trial.name() + ".trial")
        with open(trial_file, mode="w") as f:
            f.write(ciphertext)
        return trial_file

    @classmethod
    def check_trial(cls, trial_file: Path) -> Status:

        with open(trial_file, mode="r") as f:
            ciphertext = f.readline()
        cryptograph = Cryptograph(cls.__SECRET_KEY)
        plaintext = cryptograph.decrypt(ciphertext)
        trial : Trial = Trial.load(plaintext)
        if trial.status() != Status.VALID:
            return trial.status()
        trial.update()
        with open(trial_file, mode="w") as f:
            cryptograph = Cryptograph(cls.__SECRET_KEY)
            ciphertext = cryptograph.encrypt(trial.dump())
            f.write(ciphertext)
        return Status.VALID

    @classmethod
    def check_user_trial(cls) -> Status:
        trial_file = Path().home() / ".hhh.trial"
        if trial_file.exists():
            with open(trial_file, mode="r") as f:
                ciphertext = f.readline()
            cryptograph = Cryptograph(cls.__SECRET_KEY)
            plaintext = cryptograph.decrypt(ciphertext)
            trial: Trial = Trial.load(plaintext)
            if trial.status() != Status.VALID:
                return trial.status()
            trial.update()
            trial_file.unlink()
            with open(trial_file, mode="w") as f:
                cryptograph = Cryptograph(cls.__SECRET_KEY)
                ciphertext = cryptograph.encrypt(trial.dump())
                f.write(ciphertext)
            os.system(f"attrib +h {trial_file}")
            return Status.VALID
        else:
            trial = Trial.first(30)
            cryptograph = Cryptograph(cls.__SECRET_KEY)
            ciphertext = cryptograph.encrypt(trial.dump())
            with open(trial_file, mode="w") as f:
                f.write(ciphertext)
            os.system(f"attrib +h {trial_file}")
            return Status.VALID
