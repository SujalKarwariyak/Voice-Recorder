"""WAV encoding and saving (File Management module)."""

import logging
import wave

import numpy as np

from . import config

log = logging.getLogger(__name__)


def to_int16(audio):
    """Convert float32 samples in [-1, 1] to 16-bit PCM."""
    return np.clip(audio * 32767, -32768, 32767).astype(np.int16)


def write_wav(path, frames, channels, sample_rate):
    """Concatenate captured blocks and write them as a 16-bit WAV file."""
    if not frames:
        raise ValueError("No audio data was recorded.")
    pcm = to_int16(np.concatenate(frames, axis=0))
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(config.SAMPLE_WIDTH_BYTES)
        wav.setframerate(sample_rate)
        wav.writeframes(pcm.tobytes())
    log.info("Saved %s (%d samples)", path, len(pcm))
    return path


def estimate_size_mb(seconds, sample_rate, channels):
    return seconds * sample_rate * channels * config.SAMPLE_WIDTH_BYTES / (1024 * 1024)
