# Voice Recorder: Project Report

> Fill in the bracketed items (name, roll number, course, screenshots) before converting to PDF, e.g. `pandoc docs/REPORT.md -o report.pdf`.

## 1. Title Page
Voice Recorder. [Name], [Roll No.], [Course], [Institution], [Date]

## 2. Abstract
A modular Python desktop application that records microphone audio through a Tkinter GUI and saves 16-bit PCM WAV files. It uses a threaded capture module, strict input validation, logging and unit tests.

## 3. Introduction
Quick voice capture should not need heavy tools. This project provides a lightweight recorder built with Python, `sounddevice` and `numpy`.

## 4. Problem Statement
See `statement.md`.

## 5. Objectives
Record audio reliably; validate input; separate concerns into modules; log events; test the core logic without hardware.

## 6. Scope and Requirements
Functional and non-functional requirements are in `statement.md` (FR1-FR5, NFR1-NFR6).

## 7. System Design
Layered design: presentation (`gui.py`), logic (`audio_recorder.py`, `validators.py`), data (`wav_writer.py`, `file_manager.py`), cross-cutting (`config.py`, `logger.py`). See `docs/ARCHITECTURE.md` for the architecture, workflow, use case, sequence and class diagrams.

## 8. Module Description
| Module | Responsibility |
|---|---|
| config.py | Constants and limits |
| validators.py | Duration, rate, channel and filename checks |
| audio_recorder.py | Worker-thread capture, event queue |
| wav_writer.py | Float-to-PCM conversion, WAV writing, size estimate |
| file_manager.py | Directory creation, recording history |
| gui.py | Tkinter interface, queue polling |
| logger.py | Rotating file and console logging |
| main.py | Entry point |

## 9. Implementation Details
- Capture reads 1024-frame blocks and stops by frame count, so durations are exact and testable.
- Audio is held in memory as float32 (about 10 MB per minute at 44.1 kHz mono) and written on stop. The 600 s limit bounds memory use.
- WAV files are 16-bit PCM (about 5 MB per minute at 44.1 kHz mono).
- Thread safety: the worker posts events to a `queue.Queue`; only the Tk thread updates widgets.
- Closing the window during recording stops capture and saves the audio before exit.

## 10. Technologies Used
Python 3.9+, Tkinter, sounddevice, numpy, wave, logging, pytest, Git.

## 11. Testing
`pytest` runs 9 tests: validators (bounds, types, filenames), WAV round trip and empty input, size estimate, recorder with a fake stream (success and device error), and history listing with a corrupt file. Run: `python -m pytest`.

## 12. Results
[Insert screenshots: main window, recording in progress, saved status, log file.] Recorded WAV files play in standard players.

## 13. Challenges and Solutions
| Challenge | Solution |
|---|---|
| Tkinter is not thread-safe | Queue plus `after` polling |
| Testing without a microphone | Injectable stream factory and lazy import |
| Data loss on exit | `close()` stops and waits for the save |
| Empty recording crash | Explicit error, reported in the UI |

## 14. Limitations and Future Work
In-memory buffering limits length; no playback, MP3 export or device selection yet. Future work: streaming to disk, playback, device picker, level meter.

## 15. Conclusion and References
The project meets its objectives with a small, tested, modular design. References: Python docs (tkinter, wave, logging, queue), python-sounddevice docs, NumPy docs.
