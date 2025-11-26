from cuetools.types.frame_time import FrameTimeCls
import re


PEAK_PATTERN = re.compile(r'^[01]\.\d{6}$')
GAIN_PATTERN = re.compile(r'^-?\d{1,2}\.\d{2}\s*dB$')


def validate_frame_time(value: FrameTimeCls | str | int) -> FrameTimeCls:
    if isinstance(value, FrameTimeCls):
        return value

    if isinstance(value, int):
        return FrameTimeCls(frames=value)

    return FrameTimeCls.frames_f_string(value)


def serialize_frame_time(ft: FrameTimeCls) -> str:
    return ft.string


def validate_replaygain_peak(value: float | str | None) -> float | None:
    if value is None:
        return value

    if isinstance(value, float):
        if value < 0:
            raise ValueError('Expected ReplayGain album peak >= 0')
        return value

    if isinstance(value, str):
        if not PEAK_PATTERN.match(value):
            raise ValueError('Expected ReplayGain album peak match c.dddddd pattern')
        return float(value)


def validate_replaygain_gain(value: float | str | None):
    if value is None or isinstance(value, float):
        return value

    if isinstance(value, str):
        if not GAIN_PATTERN.match(value):
            raise ValueError('Expected ReplayGain album gain match [-]a.bb dB pattern')
        return float(value.split(' ')[0])
