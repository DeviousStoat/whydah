from enum import Enum
from typing import Any, NamedTuple, Self

from gargle.maybe import Maybe, maybe_next


class Category(Enum):
    NONE = 0
    MUSIC = 101
    AUDIO_BOOKS = 102
    SOUND_CLIPS = 103
    FLAC = 104
    AUDIO_OTHER = 199
    MOVIES = 201
    MOVIES_DVDR = 202
    MUSIC_VIDEOS = 203
    MOVIE_CLIPS = 204
    TV_SHOWS = 205
    VIDEO_HANDHELD = 206
    HD_MOVIES = 207
    HD_TV_SHOWS = 208
    VIDEO_3D = 209
    VIDEO_OTHER = 299
    APPLICATIONS_WINDOWS = 301
    APPLICATIONS_MAC = 302
    APPLICATIONS_UNIX = 303
    APPLICATIONS_HANDHELD = 304
    APPLICATIONS_IOS = 305
    APPLICATIONS_ANDROID = 306
    APPLICATIONS_OTHER_OS = 399
    GAMES_PC = 401
    GAMES_MAC = 402
    GAMES_PSX = 403
    GAMES_XBOX360 = 404
    GAMES_WII = 405
    GAMES_HANDHELD = 406
    GAMES_IOS = 407
    GAMES_ANDROID = 408
    GAMES_OTHER_OS = 499
    PORN_MOVIES = 501
    PORN_MOVIES_DVDR = 502
    PORN_PICTURES = 503
    PORN_GAMES = 504
    PORN_HD_MOVIES = 505
    PORN_MOVIE_CLIPS = 506
    PORN_OTHER = 599
    E_BOOKS = 601
    COMICS = 602
    PICTURES = 603
    COVERS = 604
    PHYSIBLES = 605
    OTHER = 699

    def __str__(self) -> str:
        return self.name.lower()

    @classmethod
    def from_name(cls, name: str) -> Maybe[Self]:
        upper_name = name.upper()
        return maybe_next(cat for cat in cls if cat.name == upper_name)


class PirateTorrent(NamedTuple):
    id: str
    name: str
    info_hash: str
    leechers: str
    seeders: str
    num_files: str
    size: str
    username: str
    added: str
    status: str
    category: str
    imdb: str
    anon: str | None = None

    @property
    def magnet_link(self) -> str:
        return f"magnet:?xt=urn:btih:{self.info_hash}"

    def format(self) -> str:
        return " | ".join(
            (
                self.name,
                f"leechers: {self.leechers}",
                f"seeders: {self.seeders}",
                f"username: {self.username}",
                f"status: {self.status}",
                f"imdb: {self.imdb}",
                f"magnet link: {self.magnet_link}",
            )
        )

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> Self:
        # Some of the response values can be either `int` or `str`, normalize everything
        json_data = {
            key: None if value is None else str(value)
            for key, value in json_data.items()
        }
        return cls(**json_data)
