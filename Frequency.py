import re


class Frequency(object):
    def __init__(self, inf: float, sup: float, unit: str):
        self.__inf = inf
        self.__sup = sup
        self.__unit = unit

    @property
    def inf(self):
        return self.__inf

    @property
    def sup(self):
        return self.__sup

    @property
    def unit(self):
        return self.__unit

    @property
    def name(self):
        return str(self)

    @property
    def value(self):
        if self.is_range():
            raise
        return self.__inf

    def is_range(self):
        return self.inf != self.sup

    def __str__(self):
        if self.is_range():
            return f"{self.inf}~{self.sup} {self.unit}"
        else:
            return f"{self.inf} {self.unit}"


class FrequencyBand(object):
    def __init__(self, technology: str, name: str, freq_values: list[float], duplex: str | None = None):
        self.__technology: str = technology
        self.__name: str = name
        self.__duplex: str | None = duplex
        if len(freq_values) == 4:
            self.__uplink = Frequency(freq_values[0], freq_values[1], "MHz")
            self.__downlink = Frequency(freq_values[2], freq_values[3], "MHz")
            self.__link = None
        elif len(freq_values) == 2:
            self.__link = Frequency(freq_values[0], freq_values[1], "MHz")
            self.__uplink = None
            self.__downlink = None
        elif len(freq_values) == 1:
            self.__link = Frequency(freq_values[0], freq_values[0], "MHz")
            self.__uplink = None
            self.__downlink = None
        else:
            self.__link = None
            self.__uplink = None
            self.__downlink = None

    @property
    def technology(self):
        return self.__technology

    @property
    def name(self):
        return self.__name

    @property
    def duplex(self):
        return self.__duplex

    @property
    def uplink(self) -> Frequency | None:
        return self.__uplink

    @property
    def downlink(self) -> Frequency | None:
        return self.__downlink

    @property
    def link(self) -> Frequency | None:
        return self.__link

    def is_duplex(self):
        return self.__uplink and self.__downlink

    def __str__(self):
        if self.link:
            if self.link.is_range():
                return f"频段: {self.link.inf}~{self.link.sup} {self.link.unit}"
            else:
                return f"频点: {self.link.value} {self.link.unit}"
        else:
            return f"上行: {self.uplink.inf}~{self.uplink.sup} {self.uplink.unit}, 下行: {self.downlink.inf}~{self.downlink.sup} {self.downlink.unit}"


class FrequencyManager(object):
    __all_band: list[FrequencyBand] = [
        FrequencyBand("5G NR", "n1", [1920.0, 1980.0, 2110.0, 2170.0], "FDD"),
        FrequencyBand("5G NR", "n3", [1710.0, 1785.0, 1805.0, 1880.0], "FDD"),
        FrequencyBand("5G NR", "n5", [824.0, 849.0, 869.0, 894.0], "FDD"),
        FrequencyBand("5G NR", "n8", [880.0, 915.0, 925.0, 960.0], "FDD"),
        FrequencyBand("5G NR", "n28", [703.0, 748.0, 758.0, 803.0], "FDD"),
        FrequencyBand("5G NR", "n41", [2496.0, 2690.0, 2496.0, 2690.0], "TDD"),
        FrequencyBand("5G NR", "n71", [663.0, 698.0, 617.0, 652.0], "FDD"),
        FrequencyBand("5G NR", "n77", [3300.0, 4200.0, 3300.0, 4200.0], "TDD"),
        FrequencyBand("5G NR", "n78", [3300.0, 3800.0, 3300.0, 3800.0], "TDD"),
        FrequencyBand("5G NR", "n79", [4400.0, 5000.0, 4400.0, 5000.0], "TDD"),

        FrequencyBand("4G LTE", "B1", [1920.0, 1980.0, 2110.0, 2170.0], "FDD"),
        FrequencyBand("4G LTE", "B3", [1710.0, 1785.0, 1805.0, 1880.0], "FDD"),
        FrequencyBand("4G LTE", "B5", [824.0, 849.0, 869.0, 894.0], "FDD"),
        FrequencyBand("4G LTE", "B7", [2500.0, 2570.0, 2620.0, 2690.0], "FDD"),
        FrequencyBand("4G LTE", "B8", [880.0, 915.0, 925.0, 960.0], "FDD"),
        FrequencyBand("4G LTE", "B20", [832.0, 862.0, 791.0, 821.0], "FDD"),
        FrequencyBand("4G LTE", "B28", [703.0, 748.0, 758.0, 803.0], "FDD"),
        FrequencyBand("4G LTE", "B34/B39", [2010.0, 2025.0, 2010.0, 2025.0], "TDD"),
        FrequencyBand("4G LTE", "B38", [2570.0, 2620.0, 2570.0, 2620.0], "TDD"),
        FrequencyBand("4G LTE", "B40", [2300.0, 2400.0, 2300.0, 2400.0], "TDD"),
        FrequencyBand("4G LTE", "B41", [2496.0, 2690.0, 2496.0, 2690.0], "TDD"),

        FrequencyBand("3G WCDMA", "Band 1", [1920.0, 1980.0, 2110.0, 2170.0], "FDD"),
        FrequencyBand("3G WCDMA", "Band 2", [1850.0, 1910.0, 1930.0, 1990.0], "FDD"),
        FrequencyBand("3G WCDMA", "Band 5", [824.0, 849.0, 869.0, 894.0], "FDD"),
        FrequencyBand("3G WCDMA", "Band 8", [880.0, 915.0, 925.0, 960.0], "FDD"),

        FrequencyBand("2G GSM", "GSM 900", [890.0, 915.0, 935.0, 960.0], "FDD"),
        FrequencyBand("2G GSM", "DCS 1800", [1710.0, 1785.0, 1805.0, 1880.0], "FDD"),
        FrequencyBand("2G GSM", "PCS 1900", [1850.0, 1910.0, 1930.0, 1990.0], "FDD"),

        FrequencyBand("Wi-Fi", "Wi-Fi 2.4G", [2400.0, 2483.5], None),
        FrequencyBand("Wi-Fi", "Wi-Fi 5G", [5150.0, 5850.0], None),
        FrequencyBand("Wi-Fi", "Wi-Fi 6G", [5925.0, 7125.0], None),
        FrequencyBand("Bluetooth", "Bluetooth", [2400.0, 2483.5], None),
        FrequencyBand("NFC", "NFC", [13.56], None),

        FrequencyBand("GPS", "GPS L1", [1575.42], None),
        FrequencyBand("GPS", "GPS L2", [1227.60], None),
        FrequencyBand("GPS", "GPS L5", [1176.45], None),
        FrequencyBand("北斗", "北斗 B1", [1561.098], None),
        FrequencyBand("北斗", "北斗 B2", [1207.14], None),
        FrequencyBand("北斗", "北斗 B3", [1268.52], None),
        FrequencyBand("GLONASS", "GLONASS L1", [1602.0], None),
        FrequencyBand("GLONASS", "GLONASS L2", [1246.0], None),
        FrequencyBand("Galileo", "Galileo E1", [1575.42], None),
        FrequencyBand("Galileo", "Galileo E5a", [1176.45], None),
    ]

    @classmethod
    def get_band(cls, name: str) -> FrequencyBand | None:
        for _band in cls.__all_band:
            if _band.name == name:
                return _band
        return None

    @classmethod
    def get_all_band(cls) -> list[FrequencyBand]:
        return cls.__all_band

    @classmethod
    def get_band_map(cls) -> dict[str, list[FrequencyBand]]:
        band_map: dict[str, list[FrequencyBand]] = {}
        for _band in cls.__all_band:
            if _band.technology in band_map:
                band_map[_band.technology].append(_band)
            else:
                band_map[_band.technology] = [_band]
        return band_map

    @classmethod
    def parse_freq_text(cls, freq_text: str) -> list[Frequency | FrequencyBand]:
        freqs: list[Frequency | FrequencyBand] = []
        freq_texts: list[str] = [item.strip() for item in freq_text.split(",")]
        for _freq_text in freq_texts:
            if match := re.match(r"^(\d+\.?\d*)\s+([kMG]Hz)$", _freq_text):
                freqs.append(Frequency(float(match[1]), float(match[1]), match[2]))
            elif match := re.match(r"^(\d+\.?\d*)~(\d*\.?\d+)\s+([kMG]Hz)$", _freq_text):
                freqs.append(Frequency(float(match[1]), float(match[2]), match[3]))
            else:
                band = cls.get_band(_freq_text)
                if band:
                    freqs.append(band)
        return freqs
