# Architecture and Design Diagrams

## Architecture
```mermaid
flowchart LR
  GUI[gui.py] --> VAL[validators.py]
  GUI --> REC[audio_recorder.py]
  GUI --> FM[file_manager.py]
  REC --> WAV[wav_writer.py]
  VAL --> CFG[config.py]
  REC --> CFG
  GUI & REC & WAV -.-> LOG[logger.py]
  REC --> SD[(sounddevice / microphone)]
  WAV --> DISK[(WAV file)]
```

## Workflow
```mermaid
flowchart TD
  A[Set options] --> B{Valid?}
  B -- no --> E[Show error]
  B -- yes --> C[Start worker thread]
  C --> D[Read blocks into memory]
  D --> F{Stop pressed or duration reached?}
  F -- no --> D
  F -- yes --> G[Write WAV]
  G --> H[Update status and history]
```

## Use Case
```mermaid
flowchart LR
  U((User)) --> A[Configure recording]
  U --> B[Start recording]
  U --> C[Stop recording]
  U --> D[Browse output path]
  U --> E[View recent recordings]
  B -.includes.-> V[Validate input]
```

## Sequence
```mermaid
sequenceDiagram
  participant U as User
  participant G as GUI
  participant V as Validators
  participant R as AudioRecorder
  participant W as WavWriter
  U->>G: Click Start
  G->>V: validate settings
  V-->>G: values or ValidationError
  G->>R: start(path, duration, rate, channels)
  loop each block
    R-->>G: ("progress", seconds) via queue
  end
  U->>G: Click Stop
  G->>R: stop()
  R->>W: write_wav(frames)
  R-->>G: ("done", path)
  G-->>U: status and history updated
```

## Class Diagram
```mermaid
classDiagram
  class VoiceRecorderApp { +start() +close() -_poll() }
  class AudioRecorder { +events Queue +start() +stop() +join() +is_recording }
  class ValidationError
  VoiceRecorderApp --> AudioRecorder
  VoiceRecorderApp ..> validators
  VoiceRecorderApp ..> file_manager
  AudioRecorder ..> wav_writer
  validators ..> ValidationError
```

## Threading Design
The worker thread never touches Tkinter. It posts events to a `queue.Queue`; the GUI polls it every 100 ms with `root.after`.
