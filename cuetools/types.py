from typing import Annotated

from pydantic import BeforeValidator, AfterValidator, PlainSerializer

from cuetools.validators import (
    validate_title_case,
    validate_frame_time,
    serialize_frame_time,
    validate_replaygain_peak,
    validate_replaygain_gain,
)
from cuetools.cls import FrameTimeCls

TitleCaseStr = Annotated[str, AfterValidator(validate_title_case)]

FrameTime = Annotated[
    FrameTimeCls,
    BeforeValidator(validate_frame_time),
    PlainSerializer(serialize_frame_time, return_type=str),
]

ReplayGainPeak = Annotated[float, BeforeValidator(validate_replaygain_peak)]

ReplayGainGain = Annotated[float, BeforeValidator(validate_replaygain_gain)]
