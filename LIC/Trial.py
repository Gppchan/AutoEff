import json
from datetime import datetime, timedelta

from .Status import Status


class Trial(object):

    def __init__(self, duration: int, first_date: datetime | None, last_date: datetime | None):
        self.__duration: int = duration
        self.__first_date: datetime  | None = first_date
        self.__last_date: datetime | None = last_date
        self.__expiration_date: datetime | None = None if first_date is None else first_date + timedelta(self.__duration)

    def name(self) -> str:
        return f"trial-{self.__duration}"

    @staticmethod
    def load(trial_text: str):
        trial_dict = json.loads(trial_text)
        duration = trial_dict["duration"]
        if trial_dict["first_date"] is None:
            first_date = None
        else:
            first_date = datetime.strptime(trial_dict["first_date"], "%Y-%m-%d")
        if trial_dict["last_date"] is None:
            last_date = None
        else:
            last_date = datetime.strptime(trial_dict["last_date"], "%Y-%m-%d")
        return Trial(duration, first_date, last_date)

    @staticmethod
    def first(duration: int):
        return Trial(duration, None, None)

    def dump(self):
        trial_dict : dict[str, int | str | None] = {
            "duration": self.__duration,
        }
        if self.__first_date is None:
            trial_dict["first_date"] = None
        else:
            trial_dict["first_date"] = datetime.strftime(self.__first_date, "%Y-%m-%d")
        if self.__last_date is None:
            trial_dict["last_date"] = None
        else:
            trial_dict["last_date"] = datetime.strftime(self.__last_date, "%Y-%m-%d")
        return json.dumps(trial_dict)

    def status(self) -> Status:
        if self.__is_first():
            return Status.VALID
        if self.__is_expired():
            return Status.EXPIRED
        elif self.__is_illegal():
            return Status.ILLEGAL
        else:
            return Status.VALID

    def update(self):
        if self.__is_first():
            self.__first_date = datetime.now()
        self.__last_date = datetime.now()

    def __is_first(self) -> bool:
        return self.__first_date is None

    def __is_expired(self) -> bool:
        now = datetime.now()
        return now > self.__expiration_date

    def __is_illegal(self) -> bool:
        now = datetime.now()
        return not self.__first_date <= self.__last_date <= now

    def __str__(self) -> str:
        return self.dump()

    def __repr__(self):
        return self.dump()