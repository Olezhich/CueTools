from dataclasses import dataclass, field
from typing import Optional

@dataclass(slots=True)
class TrackData:
    index : dict[str, str] = field(default_factory = lambda: {'01' : '00:00:00'})
    track : Optional[str] = None #str = '01'
    title : Optional[str] = None
    performer : Optional[str] = None
    link: Optional[str] = None

    def add_index(self, index : tuple[str, str]) -> None:
        self.index[index[0]] = index[1]

    def set_track(self, track : str) -> None:
        self.track = track

    def set_title(self, title : str) -> None:
        self.title = title

    def set_performer(self, performer : str) -> None:
        self.performer = performer

    def set_link(self, link : str) -> None:
        self.link = link

@dataclass(slots=True)
class RemData:
    genre : Optional[str] = None
    date : Optional[str] = None

@dataclass(slots=True)
class AlbumData:
    performer : Optional[str] = None
    title : Optional[str] = None
    rem : RemData = field(default_factory=RemData)
    tracks : list[TrackData] = field(default_factory=list[TrackData])

    def add_track(self, track : TrackData) -> None:
        self.tracks.append(track)

    def set_performer(self, performer : str) -> None:
        self.performer = performer

    def set_title(self, title : str) -> None:
        self.title = title

    def set_genre(self, genre : str) -> None:
        self.rem.genre = genre

    def set_date(self, date : str) -> None:
        self.rem.date = date