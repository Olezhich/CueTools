from pathlib import Path
from typing import Iterator
from cuetools.models import AlbumData, TrackData
from cuetools.parser.errors import CueParseError, CueValidationError
from cuetools.parser.handlers import title_case_handler
from cuetools.parser.lex import Token, lex

WAVE_EXTENSIONS = ['.flac', '.ape', '.wav']


def load_f_iter(cue: Iterator[str], strict_title_case: bool = False) -> AlbumData:
    """loading an object from an iterator"""
    album = AlbumData()
    current_file = None
    current_track = None

    current_line = 0

    for line in cue:
        current_line += 1
        tokens = [i for i in lex(line)]
        try:
            match tokens[0].type:
                case Token.PERFORMER:
                    performer = tokens[1]
                    if not current_track:
                        title_case_handler(
                            performer,
                            strict_title_case,
                            lambda x: setattr(album, 'performer', x),
                            album.set_performer,
                            current_line,
                            line,
                            'album performer name',
                        )
                    else:
                        title_case_handler(
                            performer,
                            strict_title_case,
                            lambda x: setattr(current_track, 'performer', x),
                            current_track.set_performer,
                            current_line,
                            line,
                            'track performer name',
                        )
                case Token.TITLE:
                    title = tokens[1]
                    if not current_track:
                        title_case_handler(
                            title,
                            strict_title_case,
                            lambda x: setattr(album, 'title', x),
                            album.set_title,
                            current_line,
                            line,
                            'album title',
                        )
                    else:
                        title_case_handler(
                            title,
                            strict_title_case,
                            lambda x: setattr(current_track, 'title', x),
                            current_track.set_title,
                            current_line,
                            line,
                            'track title',
                        )
                case Token.FILE:
                    filepath = tokens[1]
                    match filepath.type:
                        case Token.ARG_QUOTES:
                            file_type = tokens[2]
                            match file_type.type:
                                case Token.WAVE:
                                    if not any(
                                        filepath.lexeme.endswith(ext)
                                        for ext in WAVE_EXTENSIONS
                                    ):
                                        raise CueParseError(
                                            current_line,
                                            line,
                                            f"""current WAVE file type like {', '.join(f"'{i}'" for i in WAVE_EXTENSIONS)}""",
                                            file_type.lexeme,
                                            file_type.pos,
                                        )
                                case _:
                                    raise CueParseError(
                                        current_line,
                                        line,
                                        'file type tag',
                                        file_type.lexeme,
                                        file_type.pos,
                                    )

                            current_file = (  # noqa: F841 # type: ignore
                                Path(filepath.lexeme),
                                current_line,
                                line,
                                filepath.pos,
                                filepath.lexeme,
                            )
                        case _:
                            CueParseError(
                                current_line,
                                line,
                                'audiofile path',
                                filepath.lexeme,
                                filepath.pos,
                            )
                case Token.REM:
                    rem_type = tokens[1]
                    value = tokens[2]
                    match rem_type.type:
                        case Token.GENRE:
                            title_case_handler(
                                value,
                                strict_title_case,
                                lambda x: setattr(album.rem, 'genre', x),
                                album.rem.set_genre,
                                current_line,
                                line,
                                'album genre',
                            )
                        case Token.DATE:
                            try:
                                album.rem.date = int(value.lexeme)
                            except ValueError as e:
                                raise CueValidationError(
                                    current_line, line, value.pos, value.lexeme, e
                                )
                        case Token.REPLAYGAIN_ALBUM_GAIN:
                            try:
                                album.rem.replaygain_gain = value.lexeme  # type: ignore[assignment]
                            except ValueError as e:
                                raise CueValidationError(
                                    current_line, line, value.pos, value.lexeme, e
                                )
                        case Token.REPLAYGAIN_ALBUM_PEAK:
                            try:
                                album.rem.replaygain_peak = value.lexeme  # type: ignore[assignment]
                            except ValueError as e:
                                raise CueValidationError(
                                    current_line, line, value.pos, value.lexeme, e
                                )
                        case Token.REPLAYGAIN_TRACK_GAIN:
                            if not current_track:
                                raise CueParseError(
                                    current_line,
                                    line,
                                    'any TRACK tag before',
                                    tokens[0].lexeme,
                                    tokens[1].pos,
                                )
                            try:
                                current_track.rem.replaygain_gain = value.lexeme  # type: ignore[assignment]
                            except ValueError as e:
                                raise CueValidationError(
                                    current_line, line, value.pos, value.lexeme, e
                                )
                        case Token.REPLAYGAIN_TRACK_PEAK:
                            if not current_track:
                                raise CueParseError(
                                    current_line,
                                    line,
                                    'any TRACK tag before',
                                    tokens[0].lexeme,
                                    tokens[1].pos,
                                )
                            try:
                                current_track.rem.replaygain_peak = value.lexeme  # type: ignore[assignment]
                            except ValueError as e:
                                raise CueValidationError(
                                    current_line, line, value.pos, value.lexeme, e
                                )
                        case Token.DISCID:
                            ...
                        case Token.COMMENT:
                            ...
                        case _:
                            raise CueParseError(
                                current_line,
                                line,
                                'Correct REM parameter',
                                rem_type.lexeme,
                                rem_type.pos,
                            )
                case Token.TRACK:
                    if not current_file:
                        raise CueParseError(
                            current_line,
                            line,
                            'any FILE tag before',
                            tokens[1].lexeme,
                            tokens[0].pos,
                        )
                    if len(tokens) < 2 or tokens[1].type != Token.AUDIO:
                        raise CueParseError(
                            current_line,
                            line,
                            'AUDIO tag',
                            tokens[1].lexeme if len(tokens) > 1 else 'Nothing',
                            tokens[0].pos,
                        )
                    if current_track:
                        try:
                            album.add_track(current_track)
                        except ValueError as e:
                            raise CueValidationError(
                                current_line, line, 0, 'Invalid previous track', e
                            )
                    current_track = TrackData(
                        track=int(tokens[0].lexeme),
                        file=current_file[0],
                    )
                case Token.INDEX:
                    if not current_track:
                        raise CueParseError(
                            current_line,
                            line,
                            'any TRACK tag before',
                            tokens[0].lexeme,
                            tokens[1].pos,
                        )
                    index_type = int(tokens[0].lexeme)
                    if index_type == 0:
                        if current_track.index00:
                            raise CueParseError(
                                current_line,
                                line,
                                'one INDEX 00 value',
                                'dublicate INDEX 00 value',
                                tokens[0].pos,
                            )
                        current_track.index00 = tokens[1].lexeme  # type: ignore[assignment]
                    elif index_type == 1:
                        current_track.index01 = tokens[1].lexeme  # type: ignore[assignment]
                case _:
                    raise CueParseError(
                        current_line,
                        line,
                        'Correct CUE keyword',
                        tokens[0].lexeme,
                        tokens[0].pos,
                    )
        except IndexError:
            raise CueParseError(
                current_line, line, 'More tokens to parse the string correctly', line, 0
            )

    if current_track:
        album.add_track(current_track)

    return album
