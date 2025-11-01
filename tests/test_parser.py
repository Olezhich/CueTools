import cuetools


def test_load_one_track_one_file(
    cue_sample_one_file_one_track_no_quotes: str,
    cue_sample_one_file_one_track_rem_quotes: str,
    cue_sample_one_file_one_track_meta_quotes: str,
    cue_sample_one_file_one_track_rem_meta_quotes: str,
    obj_sample_one_file_one_track: cuetools.AlbumData,
):
    """basic loading case: many tracks for one cue sheet via many flac files"""
    target = obj_sample_one_file_one_track
    res = cuetools.loads(cue_sample_one_file_one_track_no_quotes)
    print(repr(res))
    assert res == target, 'loading: one_file_one_track_no_quotes'

    res = cuetools.loads(cue_sample_one_file_one_track_rem_quotes)
    print(repr(res))
    assert res == target, 'loading: one_file_one_track_rem_quotes'

    res = cuetools.loads(cue_sample_one_file_one_track_meta_quotes)
    print(repr(res))
    assert res == target, 'loading: one_file_one_track_meta_quotes'

    res = cuetools.loads(cue_sample_one_file_one_track_rem_meta_quotes)
    print(repr(res))
    assert res == target, 'loading: one_file_one_track_rem_meta_quotes'


def test_load_many_tracks_one_file(
    cue_sample_one_file_many_tracks: str,
    obj_sample_one_file_many_tracks: cuetools.AlbumData,
):
    """basic loading case: many tracks for one cue sheet via one flac file"""
    target = obj_sample_one_file_many_tracks
    res = cuetools.loads(cue_sample_one_file_many_tracks)
    print(repr(res))
    assert res == target, 'loading: cue_sample_one_file_many_tracks'


def test_dump_one_track_one_file(
    cue_sample_one_file_one_track_no_quotes: str,
    cue_sample_one_file_one_track_rem_meta_quotes: str,
    obj_sample_one_file_one_track: cuetools.AlbumData,
):
    """basic dumping case: many tracks for one cue sheet via many flac files"""
    target = cue_sample_one_file_one_track_no_quotes
    res = cuetools.dumps(obj_sample_one_file_one_track)
    assert res == target, 'dumping: one_file_one_track_no_quotes'
    target = cue_sample_one_file_one_track_rem_meta_quotes
    res = cuetools.dumps(obj_sample_one_file_one_track, quotes=True)
    assert res == target, 'dumping: one_file_one_track_rem_meta_quotes'


# def test_load_rem(obj_sample_rem, cue_sample_rem):
#     target = obj_sample_rem
#     res = cuetools.loads(cue_sample_rem)
#     assert res == target, 'loading: rem'
