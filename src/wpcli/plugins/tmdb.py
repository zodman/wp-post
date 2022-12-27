from tmdbv3api import Movie, TV


def fetch_tv(value):
    tv = TV()
    return tv.details(value).__dict__


def fetch_movie(value):
    movie = Movie()
    return movie.details(value).__dict__
