"""Central configuration constants (Configuration module)."""

from pathlib import Path

APP_TITLE = "Voice Recorder"
DEFAULT_DURATION_SECONDS = 10
MIN_DURATION_SECONDS = 1
MAX_DURATION_SECONDS = 600
SAMPLE_RATES = (8000, 16000, 22050, 44100, 48000)
DEFAULT_SAMPLE_RATE = 44100
CHANNEL_OPTIONS = {"1 (Mono)": 1, "2 (Stereo)": 2}
BLOCK_SIZE_FRAMES = 1024
SAMPLE_WIDTH_BYTES = 2  # 16-bit PCM
OUTPUT_DIR = Path("recordings")
LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "voice_recorder.log"
