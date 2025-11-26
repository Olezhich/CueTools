from typing import Annotated

from pydantic import BeforeValidator, PlainSerializer

from cuetools.types.validators import (
    validate_frame_time,
    serialize_frame_time,
    validate_replaygain_peak,
    validate_replaygain_gain,
)
from cuetools.types.frame_time import FrameTimeCls

FrameTime = Annotated[
    FrameTimeCls,
    BeforeValidator(validate_frame_time),
    PlainSerializer(serialize_frame_time, return_type=str),
]

ReplayGainPeak = Annotated[float, BeforeValidator(validate_replaygain_peak)]

ReplayGainGain = Annotated[float, BeforeValidator(validate_replaygain_gain)]
