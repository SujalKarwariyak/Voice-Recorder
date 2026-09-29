"""Output directory handling and recording history (File Management module)."""

import logging
import wave
from pathlib import Path

from . import config

log = logging.getLogger(__name__)


def ensure_parent(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def file_size_mb(path):
    return Path(path).stat().st_size / (1024 * 1024)


def list_recordings(directory=None):
    """Return metadata for each valid WAV file, newest first."""
    directory = Path(directory or config.OUTPUT_DIR)
    if not directory.is_dir():
        return []
    items = []
    for wav_path in sorted(directory.glob("*.wav"), key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            with wave.open(str(wav_path), "rb") as wav:
                seconds = wav.getnframes() / wav.getframerate()
                items.append({"name": wav_path.name, "path": wav_path, "seconds": seconds,
                              "size_mb": file_size_mb(wav_path)})
        except (wave.Error, EOFError, OSError):
            log.warning("Skipping unreadable file %s", wav_path)
    return items
