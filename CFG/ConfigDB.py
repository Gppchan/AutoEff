from pathlib import Path
import sqlite3 as sqlite


class ConfigDB(object):
    def __init__(self, db_file: Path):
        self.file = db_file
        self.__db = sqlite.connect(self.file)
        self.__cursor = self.__db.cursor()
        self.create_section("Global")

    def select_section_names(self) -> list[str]:
        sql: str = f"""
        SELECT name FROM sqlite_master WHERE type="table" ORDER BY name
"""
        self.__cursor.execute(sql)
        outcome = self.__cursor.fetchall()
        return [_name for _name, in outcome]

    def has_section(self, section_name: str) -> bool:
        section_names = self.select_section_names()
        return section_name in section_names

    def create_section(self, section_name: str) -> None:
        if self.has_section(section_name):
            return None

        sql: str = f"""
CREATE TABLE IF NOT EXISTS {section_name} (
    key Text Not Null UNIQUE,
    value Text Not Null
)
"""
        self.__cursor.execute(sql)
        self.__db.commit()

    def drop_section(self, section_name: str) -> None:
        if not self.has_section(section_name):
            return None

        sql: str = f"""
        DROP TABLE {section_name}
"""
        self.__cursor.execute(sql)

    def select_section(self, section_name: str = "") -> dict[str, str]:
        if not section_name:
            section_name = "Global"
        if not self.has_section(section_name):
            return {}

        sql: str = f"""
        SELECT key, value FROM {section_name}
"""
        self.__cursor.execute(sql)
        outcome = self.__cursor.fetchall()
        return {_key: _value for _key, _value in outcome}

    def has_key(self, key: str, section_name: str = "") -> bool:
        if not self.has_section(section_name):
            return False
        section = self.select_section(section_name)
        return key in section

    def select_key(self, key: str, section_name: str = "") -> str:
        if not section_name:
            section_name = "Global"
        if not self.has_key(key, section_name):
            return ""

        sql: str = f"""
        SELECT value FROM {section_name} WHERE key = "{key}"
"""
        self.__cursor.execute(sql)
        outcome = self.__cursor.fetchall()
        return outcome[0][0] if outcome else ""

    def insert_key(self, key: str, value: str, section_name: str = "") -> None:
        if not section_name:
            section_name = "Global"
        if self.has_key(key, section_name):
            return None

        sql: str = f"""
        INSERT INTO {section_name} (key, value) VALUES ("{key}", "{value}")
"""
        self.__cursor.execute(sql)
        self.__db.commit()

    def delete_key(self, key: str, section_name: str = "") -> None:
        if not section_name:
            section_name = "Global"
        if not self.has_key(key, section_name):
            return None

        sql: str = f"""
        DELETE FROM {section_name} WHERE key = "{key}"
"""
        self.__cursor.execute(sql)

    def update_key(self, key: str, value: str, section_name: str = "") -> None:
        if not section_name:
            section_name = "Global"
        if not self.has_key(key, section_name):
            return None

        sql: str = f"""
        UPDATE {section_name} SET value = "{value}" WHERE key = "{key}"
"""
        self.__cursor.execute(sql)

    def is_section(self, section: str) -> bool:
        sql: str = f"""
        PRAGMA table_info({section})
"""
        self.__cursor.execute(sql)
        outcome = self.__cursor.fetchall()
        names = [_name for _, _name, *_ in outcome]
        return names[0] == "key"

    def close(self) -> None:
        self.__db.close()
        self.__cursor.close()

    def __str__(self) -> str:
        text_list: list[str] = []
        section_names = self.select_section_names()
        for _name in section_names:
            text_list.append(f"[{_name}]")
            section = self.select_section(_name)
            for _key, _value in section.items():
                text_list.append(f"{_key} = {_value}")
        return "\n".join(text_list)

    def __repr__(self) -> str:
        return str(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
