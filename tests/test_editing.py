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


# --- reparación de movimiento -------------------------------------------------

import numpy as np

from ugc_agency.editing.repair import Join, detect_joins, detect_pulldown, join_graph


def _motion(n=300, seed=0):
    rng = np.random.default_rng(seed)
    return rng.uniform(2.0, 4.0, n)


def test_detect_pulldown_every_fifth_frame():
    d = _motion()
    d[5::5] = 0.05          # 24 -> 30 fps: un duplicado cada 5
    assert detect_pulldown(d) == 5
    assert detect_pulldown(_motion()) is None


def test_detect_joins_with_intruder_frames():
    d = _motion()
    d[100] = 40             # unión limpia
    d[200], d[203] = 35, 25  # unión con 3 cuadros intrusos (200-202)
    joins = detect_joins(d, fps=24)
    assert [(j.end_a, j.start_b) for j in joins] == [(100, 100), (200, 203)]


def test_join_graph_keeps_total_duration():
    graph, out_frames = join_graph(300, 24.0, [Join(100, 100), Join(200, 203)], fade_frames=6)
    assert out_frames == 300   # el audio no se toca, así que la duración debe ser idéntica
    assert sum("xfade" in g for g in graph) == 2


# --- compositor ---------------------------------------------------------------

from ugc_agency.editing.compose import find_phrase, resolve_cue


def test_phrase_cues_ignore_accents_and_punctuation():
    words = [Word(0.0, 0.3, "Escríbenos,"), Word(0.4, 0.6, "FDA"), Word(0.7, 1.1, "2026."),
             Word(2.0, 2.3, "escribenos")]
    assert find_phrase(words, "escribenos fda") == (0.0, 0.6)
    assert find_phrase(words, "Escríbenos", occurrence=2) == (2.0, 2.3)
    assert resolve_cue({"phrase": "fda 2026", "edge": "end", "offset": 0.2}, words, 10, "start") == 1.3
    assert resolve_cue("video_end", words, 10, "start") == 10
