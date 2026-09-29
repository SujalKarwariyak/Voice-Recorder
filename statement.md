# Problem Statement

## Problem
Capturing a short voice note on a desktop usually needs a heavy audio editor. Beginners also struggle with sample rates, channel counts and file formats.

## Objective
Build a small, reliable desktop voice recorder in Python that records microphone audio with a simple GUI and saves it as a standard WAV file.

## Scope
**In scope:** timed or open-ended recording, sample rate and mono/stereo selection, custom or auto-generated filenames, input validation, logging, and a list of recent recordings.
**Out of scope:** editing, compression (MP3), cloud upload, noise removal.

## Users
Students and general users who want a quick way to capture audio.

## Major Modules
1. **Recording**: `audio_recorder.py` (threaded capture, event queue)
2. **Configuration and Validation**: `config.py`, `validators.py`
3. **File Management**: `wav_writer.py`, `file_manager.py` (WAV encoding, history)

Supporting modules: `gui.py` (presentation), `logger.py`, `main.py`.

## Functional Requirements
- FR1 Record for 1-600 seconds or until Stop is pressed.
- FR2 Choose sample rate (8000-48000 Hz) and mono/stereo.
- FR3 Save 16-bit PCM WAV with a custom or timestamped name.
- FR4 Reject invalid input with a clear message.
- FR5 Show progress, status and recent recordings.

## Non-Functional Requirements
- NFR1 **Reliability:** an error must never crash the app or lose captured audio on exit.
- NFR2 **Responsiveness:** the UI stays responsive because capture runs on a worker thread; only the Tk thread touches widgets.
- NFR3 **Maintainability:** GUI, capture, validation and file code are separate modules with unit tests.
- NFR4 **Observability:** all events and errors go to a rotating log file.
- NFR5 **Portability:** runs on Windows, macOS and Linux with Python 3.9+.
- NFR6 **Usability:** sensible defaults; a one-click start.

## Success Criteria
All unit tests pass, a recorded WAV plays in a standard player, and invalid input is rejected with a message.
