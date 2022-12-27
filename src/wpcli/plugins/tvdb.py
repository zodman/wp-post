import tvdb_v4_official
from ..conf import TVDB_API_KEY


def fetch(value):
    tvdb = tvdb_v4_official.TVDB(TVDB_API_KEY)
    series = tvdb.get_series_extends(value)
    assert False, series
