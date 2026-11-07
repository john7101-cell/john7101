"""Pruebas de la lógica del editor (sin ffmpeg ni Whisper)."""

from pathlib import Path

from ugc_agency.editing.analysis import Segment, Word, find_fillers, find_glitch_shots, find_retakes
from ugc_agency.editing.editor import write_srt
from ugc_agency.editing.media import direct_download_url
from ugc_agency.editing.timeline import Cut, keep_segments, map_time


def test_keep_segments_and_map_time():
    keeps = keep_segments(10.0, [Cut(2, 4, "pausa"), Cut(3.5, 5, "x"), Cut(9.95, 10, "tiny")])
    assert keeps == [(0.0, 2), (5, 9.95)]
    assert map_time(1.0, keeps) == 1.0
    assert map_time(3.0, keeps) is None
    assert map_time(6.0, keeps) == 3.0


def test_fillers_and_retakes():
    w = lambda s, e, t: Word(s, e, t)
    segs = [
        Segment(0, 2, "and my feet are killing me", [w(0, .5, "and"), w(.5, 1, "um,")]),
        Segment(2.5, 5, "And my feet are killing me, honestly.", [w(2.5, 3, "And")]),
        Segment(5, 7, "this cup is great", []),
    ]
    assert [x.text for x in find_fillers(segs)] == ["um,"]
    assert find_retakes(segs) == [segs[0]]


def test_glitch_shots_ignore_first_and_last():
    scenes = [(0, 0.1), (0.1, 3), (3, 3.07), (3.07, 8), (8, 8.1)]
    assert find_glitch_shots(scenes) == [(3, 3.07)]


def test_srt_breaks_on_punctuation_and_skips_cut_words(tmp_path: Path):
    words = [Word(0, .3, "Okay,"), Word(.4, .6, "so"), Word(.6, .8, "um"), Word(3, 3.4, "this"),
             Word(3.4, 3.8, "works.")]
    keeps = [(0, 1), (2.9, 4)]
    n = write_srt(tmp_path / "a.srt", [Segment(0, 4, "", words)], keeps)
    text = (tmp_path / "a.srt").read_text()
    assert n == 2 and "OKAY," in text and "UM" not in text and "SO THIS WORKS." in text


def test_direct_download_urls():
    assert direct_download_url("https://drive.google.com/file/d/AbC_1-2/view?usp=sharing") == \
        "https://drive.usercontent.google.com/download?id=AbC_1-2&export=download&confirm=t"
    assert direct_download_url("https://www.dropbox.com/s/x/v.mp4?dl=0").endswith("dl=1")
