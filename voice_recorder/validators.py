"""Input validation (Configuration and Validation module)."""

from datetime import datetime
from pathlib import Path

from . import config


class ValidationError(ValueError):
    """Raised when a user supplied setting is invalid."""


def validate_duration(value):
    """Return the duration in seconds as a float within the allowed range."""
    try:
        duration = float(value)
    except (TypeError, ValueError):
        raise ValidationError("Duration must be a number.") from None
    if not config.MIN_DURATION_SECONDS <= duration <= config.MAX_DURATION_SECONDS:
        raise ValidationError(
            f"Duration must be between {config.MIN_DURATION_SECONDS} "
            f"and {config.MAX_DURATION_SECONDS} seconds."
        )
    return duration


def validate_sample_rate(value):
    try:
        rate = int(value)
    except (TypeError, ValueError):
        raise ValidationError("Sample rate must be an integer.") from None
    if rate not in config.SAMPLE_RATES:
        raise ValidationError(f"Sample rate must be one of {config.SAMPLE_RATES}.")
    return rate


def validate_channels(label):
    try:
        return config.CHANNEL_OPTIONS[label]
    except KeyError:
        raise ValidationError("Channels must be Mono or Stereo.") from None


def resolve_filename(name, now=None):
    """Return a Path ending in .wav; generate a timestamped name if blank."""
    name = (name or "").strip()
    if not name:
        stamp = (now or datetime.now()).strftime("%Y%m%d_%H%M%S")
        return config.OUTPUT_DIR / f"recording_{stamp}.wav"
    path = Path(name)
    if path.suffix.lower() != ".wav":
        path = path.with_name(path.name + ".wav")
    return path
