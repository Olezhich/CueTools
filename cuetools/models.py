from dataclasses import dataclass, field

@dataclass(slots=True)
class TrackData:
    """
    Contains metadata of one track in cue sheet

    :ivar index: The index of track, corresponds to the line like *'INDEX 01 00:00:00'*
    :ivar track: Track number string, corresponds to rhe line like *'TRACK 01 AUDIO'*
    :ivar title: Track title
    :ivar performer: Track performer
    :ivar link: Path to the audio file with this track (to flac, ape or etc.) relative to the cue sheet file
    """

    index : dict[str, str] = field(default_factory = lambda: {'01' : '00:00:00'})
    track : str | None = None
    title : str | None = None
    performer : str | None = None
    link: str | None = None

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
    """
    Contains comment fields of cue sheet, corresponds to the *'REM'* lines

    :ivar genre: Album genre
    :ivar date: Album release date
    :ivar replaygain_album_gain: Album replay gain in db
    :ivar replaygain_album_peak: Album peak value in db
    """

    genre : str | None = None
    date : str | None = None
    replaygain_album_gain : str | None = None
    replaygain_album_peak : str | None = None

@dataclass(slots=True)
class AlbumData:
    """
    Contains metadata of whole album in cue sheet

    :ivar performer: Album performer
    :ivar title: Album title
    :ivar rem: Album additional rem meta
    :ivar tracks: Tracks list of this album
    """

    performer : str | None = None
    title : str | None = None
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

    def set_gain(self, gain : str) -> None:
        self.rem.replaygain_album_gain = gain

    def set_peak(self, peak : str) -> None:
        self.rem.replaygain_album_peak = peak