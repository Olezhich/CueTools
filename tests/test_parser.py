# import pytest

# import cuetools
# from tests import *


# def test_load_one_track_one_file(cue_sample_one_file_one_track_no_quotes,
#                                  cue_sample_one_file_one_track_rem_quotes,
#                                  cue_sample_one_file_one_track_meta_quotes,
#                                  cue_sample_one_file_one_track_rem_meta_quotes,
#                                  obj_sample_one_file_one_track):
#     """basic loading case: many tracks for one cue sheet via many flac files"""
#     target = obj_sample_one_file_one_track
#     res = cuetools.loads(cue_sample_one_file_one_track_no_quotes)
#     assert res == target , 'loading: one_file_one_track_no_quotes'
#     res = cuetools.loads(cue_sample_one_file_one_track_rem_quotes)
#     assert res == target, 'loading: one_file_one_track_rem_quotes'
#     res = cuetools.loads(cue_sample_one_file_one_track_meta_quotes)
#     assert res == target, 'loading: one_file_one_track_meta_quotes'
#     res = cuetools.loads(cue_sample_one_file_one_track_rem_meta_quotes)
#     assert res == target, 'loading: one_file_one_track_rem_meta_quotes'

# def test_load_many_tracks_one_file(cue_sample_one_file_many_tracks,
#                                    obj_sample_one_file_many_tracks):
#     """basic loading case: many tracks for one cue sheet via one flac file"""
#     target = obj_sample_one_file_many_tracks
#     res = cuetools.loads(cue_sample_one_file_many_tracks)
#     assert res == target, 'loading: cue_sample_one_file_many_tracks'

# def test_dump_one_track_one_file(cue_sample_one_file_one_track_no_quotes,
#                                  cue_sample_one_file_one_track_rem_meta_quotes,
#                                  obj_sample_one_file_one_track):
#     """basic dumping case: many tracks for one cue sheet via many flac files"""
#     target = cue_sample_one_file_one_track_no_quotes
#     res = cuetools.dumps(obj_sample_one_file_one_track)
#     assert res == target, 'dumping: one_file_one_track_no_quotes'
#     target = cue_sample_one_file_one_track_rem_meta_quotes
#     res = cuetools.dumps(obj_sample_one_file_one_track, quotes=True)
#     assert res == target, 'dumping: one_file_one_track_rem_meta_quotes'

# def test_load_rem(obj_sample_rem, cue_sample_rem):
#     target = obj_sample_rem
#     res = cuetools.loads(cue_sample_rem)
#     assert res == target, 'loading: rem'
