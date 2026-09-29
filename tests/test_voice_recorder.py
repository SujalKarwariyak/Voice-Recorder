import wave
from datetime import datetime

import numpy as np
import pytest

from voice_recorder import file_manager, validators, wav_writer
from voice_recorder.audio_recorder import AudioRecorder


class FakeStream:
    def __init__(self, channels):
        self.channels, self.closed = channels, False

    def start(self): pass
    def stop(self): pass
    def close(self): self.closed = True
    def read(self, n): return np.full((n, self.channels), 0.5, dtype="float32"), False


def run(recorder, path, duration, rate=8000, ch=1):
    recorder.start(path, duration, rate, ch)
    recorder.join(5)
    events = []
    while not recorder.events.empty():
        events.append(recorder.events.get())
    return events


def test_duration_valid_and_bounds():
    assert validators.validate_duration("5") == 5.0
    for bad in ("0", "601", "abc", None):
        with pytest.raises(validators.ValidationError):
            validators.validate_duration(bad)


def test_sample_rate_and_channels():
    assert validators.validate_sample_rate("44100") == 44100
    with pytest.raises(validators.ValidationError):
        validators.validate_sample_rate("12345")
    assert validators.validate_channels("2 (Stereo)") == 2
    with pytest.raises(validators.ValidationError):
        validators.validate_channels("5")


def test_filename_rules(tmp_path):
    assert validators.resolve_filename("Test.WAV").name == "Test.WAV"
    assert validators.resolve_filename("note").name == "note.wav"
    auto = validators.resolve_filename("", datetime(2026, 1, 2, 3, 4, 5))
    assert auto.name == "recording_20260102_030405.wav"


def test_write_wav_roundtrip(tmp_path):
    p = tmp_path / "a.wav"
    wav_writer.write_wav(p, [np.zeros((100, 2), dtype="float32")], 2, 16000)
    with wave.open(str(p)) as w:
        assert (w.getnchannels(), w.getframerate(), w.getnframes()) == (2, 16000, 100)


def test_write_wav_empty_raises(tmp_path):
    with pytest.raises(ValueError):
        wav_writer.write_wav(tmp_path / "x.wav", [], 1, 8000)


def test_size_estimate():
    assert wav_writer.estimate_size_mb(60, 44100, 1) == pytest.approx(5.05, abs=0.01)


def test_recorder_fixed_duration(tmp_path):
    rec = AudioRecorder(lambda r, c: FakeStream(c))
    events = run(rec, tmp_path / "out.wav", 1)
    assert events[-1][0] == "done"
    with wave.open(str(tmp_path / "out.wav")) as w:
        assert w.getnframes() >= 8000


def test_recorder_reports_error():
    def boom(r, c):
        raise RuntimeError("No audio input device was found.")
    events = run(AudioRecorder(boom), "x.wav", 1)
    assert events[-1][0] == "error"


def test_list_recordings_skips_bad_files(tmp_path):
    wav_writer.write_wav(tmp_path / "ok.wav", [np.zeros((800, 1), dtype="float32")], 1, 8000)
    (tmp_path / "bad.wav").write_bytes(b"not a wav")
    items = file_manager.list_recordings(tmp_path)
    assert [i["name"] for i in items] == ["ok.wav"]
    assert items[0]["seconds"] == pytest.approx(0.1)
