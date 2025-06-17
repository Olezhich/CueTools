import pytest

import cuelogic
from tests import cue_sample_one_file_one_track, obj_sample_one_file_one_track


def test_load_one_track_one_file(cue_sample_one_file_one_track, obj_sample_one_file_one_track):
    res = cuelogic.load(cue_sample_one_file_one_track)
    assert res == obj_sample_one_file_one_track