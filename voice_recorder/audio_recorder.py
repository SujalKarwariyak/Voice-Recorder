"""Audio capture (Recording module). No GUI code lives here."""

import logging
import queue
import threading

from . import config, wav_writer

log = logging.getLogger(__name__)


def _default_stream_factory(sample_rate, channels):
    import sounddevice as sd  # imported lazily so tests need no audio hardware

    if not sd.query_devices(kind="input"):
        raise RuntimeError("No audio input device was found.")
    return sd.InputStream(samplerate=sample_rate, channels=channels,
                          dtype="float32", blocksize=config.BLOCK_SIZE_FRAMES)


class AudioRecorder:
    """Records on a worker thread and reports through a thread-safe queue.

    Events put on ``events``: ("progress", seconds), ("done", path), ("error", exc).
    """

    def __init__(self, stream_factory=_default_stream_factory):
        self._factory = stream_factory
        self._stop = threading.Event()
        self._thread = None
        self.events = queue.Queue()

    @property
    def is_recording(self):
        return self._thread is not None and self._thread.is_alive()

    def start(self, path, duration, sample_rate, channels):
        if self.is_recording:
            raise RuntimeError("Already recording.")
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._run, args=(path, duration, sample_rate, channels), daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()

    def join(self, timeout=None):
        if self._thread:
            self._thread.join(timeout)

    def _run(self, path, duration, sample_rate, channels):
        frames, captured, stream = [], 0, None
        limit = None if duration is None else int(duration * sample_rate)
        try:
            stream = self._factory(sample_rate, channels)
            stream.start()
            log.info("Recording started (%s Hz, %s ch)", sample_rate, channels)
            while not self._stop.is_set() and (limit is None or captured < limit):
                data, overflowed = stream.read(config.BLOCK_SIZE_FRAMES)
                if overflowed:
                    log.warning("Input overflow: some audio may have been dropped")
                frames.append(data.copy())
                captured += len(data)
                self.events.put(("progress", captured / sample_rate))
            stream.stop()
            wav_writer.write_wav(path, frames, channels, sample_rate)
            self.events.put(("done", path))
        except Exception as exc:  # reported to the GUI, never raised on the worker
            log.exception("Recording failed")
            self.events.put(("error", exc))
        finally:
            if stream is not None:
                try:
                    stream.close()
                except Exception:
                    log.debug("Stream close failed", exc_info=True)
