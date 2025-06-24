import pytest

import cuelogic
from tests import *


def test_load_one_track_one_file(cue_sample_one_file_one_track_no_quotes,
                                 cue_sample_one_file_one_track_rem_quotes,
                                 cue_sample_one_file_one_track_meta_quotes,
                                 cue_sample_one_file_one_track_rem_meta_quotes,
                                 obj_sample_one_file_one_track):
    """base case: many tracks for one cue sheet via many flac files"""
    target = obj_sample_one_file_one_track
    res = cuelogic.loads(cue_sample_one_file_one_track_no_quotes)
    assert res == target , 'cue_sample_one_file_one_track_no_quotes'
    res = cuelogic.loads(cue_sample_one_file_one_track_rem_quotes)
    assert res == target, 'cue_sample_one_file_one_track_rem_quotes'
    res = cuelogic.loads(cue_sample_one_file_one_track_meta_quotes)
    assert res == target, 'cue_sample_one_file_one_track_meta_quotes'
    res = cuelogic.loads(cue_sample_one_file_one_track_rem_meta_quotes)
    assert res == target, 'cue_sample_one_file_one_track_rem_meta_quotes'

def test_load_many_tracks_one_file():
    """base case: many tracks for one cue sheet via one flac file"""
    ...