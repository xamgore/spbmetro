import re
from typing import Dict, List

from notebook.stations import abbreviations as Abbrs
from structure import Subway


class Restore:
    _digits = re.compile('\d+')
    _optional_or_digits = re.compile('(' + '|'.join(Abbrs.optional) + ')', re.I)
    _restore_dict = None


    @classmethod
    def without_digits(cls, title: str) -> str:
        return cls._digits.sub('', title).strip()


    @classmethod
    def preprocess(cls, title: str) -> str:
        return cls._optional_or_digits.sub('', title).strip().lower()


    @classmethod
    def _prepare_restore_dict(cls, station_titles: List[str]) -> Dict[str, str]:
        return {cls.preprocess(title): title for title in station_titles}


    @classmethod
    def get(cls, title):
        if cls._restore_dict is None:
            stations = [cls.without_digits(st) for st in Subway.load().stations.keys()]
            cls._restore_dict = cls._prepare_restore_dict(stations)

        return cls._restore_dict[cls.preprocess(title)]
