# Voice Recorder with GUI

A simple, professional desktop voice recording application built with Python, Tkinter, SoundDevice, and NumPy. This application provides an easy-to-use graphical interface for recording audio and saving it as WAV files with multiple quality and format options.

## Overview

Voice Recorder is a lightweight, cross-platform desktop application designed for recording audio from your microphone. Whether you need to record voice notes, interviews, podcasts, or music, this application provides flexible recording options with real-time progress feedback. The application runs natively on Windows, macOS, and Linux without requiring any external audio software.

## How It Works

### Recording Process

1. **Audio Input Capture**: The application uses the `sounddevice` library to access and capture audio data from the system's microphone or audio input device in real-time.

2. **Audio Buffering**: Captured audio is processed in 1024-byte blocks (blocksize configuration) and stored as float32 data in memory.

3. **Audio Processing**: During recording, audio samples are accumulated in frames. When recording stops or duration limit is reached, the frames are concatenated together.

4. **Format Conversion**: The float32 audio data (range -1.0 to 1.0) is converted to 16-bit PCM integer format (range -32768 to 32767) using NumPy for standard WAV format compatibility.

5. **File Storage**: The converted audio is written to a WAV file using Python's built-in `wave` module with the specified sample rate, number of channels, and bit depth.

### Threading Architecture

The application uses Python's `threading` module to handle recording in a background thread, preventing the GUI from freezing:

- **Main Thread**: Handles all GUI operations and user interactions using Tkinter
- **Recording Thread**: Runs the actual audio capture and file writing operations
- **Thread Communication**: Uses `threading.Event` objects for safe stop signal communication between threads

### User Interface Components

The GUI is built with `tkinter.ttk` (themed Tkinter) and includes:

- **Title and Labels**: Clear labeling of all input fields
- **Duration Control**: Spinbox widget for selecting recording duration (1-600 seconds)
- **Unlimited Mode Checkbox**: Toggle for continuous recording until manually stopped
- **Sample Rate Selection**: Dropdown menu for choosing audio quality (8kHz to 48kHz)
- **Channel Selection**: Dropdown for mono or stereo recording
- **Filename Input**: Text entry for custom output filename with browse button for directory selection
- **Status Display**: Real-time status indicator that changes color based on application state
- **Progress Bar**: Visual progress indicator that switches between determinate (timed recording) and indeterminate (unlimited recording) modes
- **Elapsed Time Display**: Shows MM:SS format for unlimited recordings
- **Control Buttons**: Start Recording, Stop Recording, and Exit buttons with proper state management

## Features

### Core Recording Features

- **Fixed-Duration Recording**: Record for 1 to 600 seconds with automatic stop
- **Unlimited Recording Mode**: Record indefinitely until manually stopped
- **Multiple Sample Rates**: 8kHz, 16kHz, 22.05kHz, 44.1kHz, and 48kHz for different quality needs
- **Mono and Stereo Recording**: Single or dual-channel audio capture
- **Real-Time Progress Tracking**: Visual progress bar and elapsed time display
- **Flexible File Management**: Custom output paths, automatic filename generation with timestamps
- **Error Handling**: Comprehensive error detection and user-friendly error messages
- **Device Detection**: Automatic microphone detection with fallback error messages
- **State Management**: Proper enabling/disabling of controls during recording

### Technical Features

- **16-bit PCM Encoding**: Standard audio format for maximum compatibility
- **Float32 Audio Processing**: High-precision audio capture and processing
- **Cross-Platform Compatibility**: Works on Windows, macOS, and Linux
- **Automatic Directory Creation**: Creates output directories if they don't exist
- **Thread-Safe Operations**: Safe communication between GUI and recording threads
- **Resource Cleanup**: Proper stream closure and error recovery

## Architecture and Technologies

### Dependencies

#### sounddevice (>= 0.4.6)
- **Purpose**: Cross-platform audio input/output library
- **Usage**: Queries available audio devices, creates input streams, reads audio data
- **Why Used**: No compilation required, precompiled binaries, excellent cross-platform support
- **How It Works**: Wraps operating system audio APIs (WASAPI on Windows, ALSA on Linux, CoreAudio on macOS)

#### numpy (>= 1.24.0)
- **Purpose**: Numerical computing and array operations
- **Usage**: Audio data conversion from float32 to int16, array concatenation, audio scaling
- **Why Used**: Fast vectorized operations for audio processing
- **How It Works**: Provides efficient C-backed array operations for audio manipulation

#### tkinter
- **Purpose**: Graphical user interface creation
- **Usage**: All GUI components, window management, event handling
- **Status**: Built-in with Python (usually included)
- **How It Works**: Provides bindings to the Tk GUI toolkit

#### wave (Python Standard Library)
- **Purpose**: WAV file creation and writing
- **Usage**: Opens WAV files for writing, configures format, writes audio data
- **How It Works**: Encapsulates audio data in WAV file format with proper headers

#### threading (Python Standard Library)
- **Purpose**: Background thread execution
- **Usage**: Runs recording in separate thread to prevent GUI freezing
- **How It Works**: Manages thread lifecycle and synchronization

### File Structure

```
Voice-Recorder/
├── voice_recorder_gui.py      # 289 lines - Main application with VoiceRecorderApp class
├── run.bat                    # 76 lines - Windows launcher and setup automation
├── SETUP.txt                  # Setup and installation instructions
├── requirements.txt           # Python package dependencies
├── README.md                  # This documentation
└── LICENSE                    # Project license
```

### Code Structure (voice_recorder_gui.py)

**VoiceRecorderApp Class Methods:**

- `__init__(root)`: Initializes the application, sets up window properties, and invokes UI setup
- `setup_ui()`: Creates all GUI components using Tkinter widgets
- `toggle_unlimited()`: Enables/disables duration spinbox based on unlimited mode checkbox
- `browse_file()`: Opens file dialog for user to select output location
- `start_recording()`: Validates inputs, configures UI state, starts recording thread
- `record(filename, duration, sample_rate, channels)`: Core recording method that captures, processes, and saves audio
- `update_recording_status(elapsed, duration)`: Updates progress bar and elapsed time display
- `recording_finished(filename, error)`: Handles post-recording cleanup and user feedback
- `stop_recording()`: Sets stop event to halt recording
- `close()`: Safely closes application, ensuring recording is stopped first

## Requirements

- **Python**: 3.7 or later
- **Operating System**: Windows, macOS, or Linux
- **Microphone**: Connected and available to the operating system
- **Tkinter**: Usually included with Python
- **Audio Drivers**: Working audio device drivers for your OS

## Installation

### Windows

1. Install Python 3.9 or later from [python.org](https://www.python.org/downloads/)
2. **Important**: During installation, check **"Add Python to PATH"**
3. Download all project files into a single folder
4. Double-click `run.bat` to start the automated setup and launch

**What run.bat Does:**
- Checks Python installation and version
- Verifies pip is installed
- Installs sounddevice and numpy from requirements.txt
- Detects connected audio input devices
- Launches the application
- Displays helpful error messages if any step fails

### macOS

```bash
# Install dependencies
python3 -m pip install -r requirements.txt

# Run the application
python3 voice_recorder_gui.py
```

### Linux (Ubuntu/Debian)

```bash
# Install Tkinter if not already installed
sudo apt install python3-tk

# Install Python dependencies
python3 -m pip install -r requirements.txt

# Run the application
python3 voice_recorder_gui.py
```

### Linux (Fedora/RHEL)

```bash
# Install Tkinter if not already installed
sudo dnf install python3-tkinter

# Install Python dependencies
python3 -m pip install -r requirements.txt

# Run the application
python3 voice_recorder_gui.py
```

## Usage

### Basic Recording Workflow

1. **Launch Application**: Double-click `run.bat` (Windows) or run `python voice_recorder_gui.py` (Mac/Linux)

2. **Configure Settings**:
   - Select recording duration (1-600 seconds) or enable unlimited mode
   - Choose sample rate based on quality needs
   - Select mono or stereo channels
   - Optionally enter custom filename or leave blank for auto-generation

3. **Start Recording**:
   - Click "Start Recording" button
   - Speak or perform audio into your microphone
   - Watch real-time progress feedback

4. **Stop Recording**:
   - Click "Stop Recording" button manually, or
   - Wait for automatic stop when timed duration expires

5. **Save File**:
   - Recording automatically saves to specified location
   - Success message confirms file location and size
   - File is ready to use in other applications

### Recording Modes

**Fixed-Duration Mode**:
- Select duration from spinbox (1-600 seconds)
- Checkbox "Record until I click Stop" should be unchecked
- Recording stops automatically when duration expires
- Progress bar shows percentage complete
- Best for predictable, time-limited sessions

**Unlimited Mode**:
- Check "Record until I click Stop" checkbox
- Duration spinbox becomes disabled
- Recording continues until Stop button is clicked
- Progress bar shows continuous animation
- Elapsed time displays in MM:SS format
- Best for variable-length content

### Advanced Features

**Custom Output Location**:
- Click "Browse" button next to filename field
- Select desired folder for saving
- Enter custom filename (with or without .wav extension)
- Application automatically creates directories if needed

**Auto-Generated Filenames**:
- Leave filename field empty
- Application generates: `recording_YYYYMMDD_HHMMSS.wav`
- Example: `recording_20240115_143022.wav`
- Ensures unique filenames for each recording

## Audio Quality Settings

### Sample Rate Comparison

| Rate | Quality Level | File Size (1 min) | Use Cases |
|------|---------------|-------------------|-----------|
| 8 kHz | Very Low | ~0.5 MB | Phone quality, archived speech |
| 16 kHz | Low | ~1.0 MB | Voice memos, interviews, speech recognition |
| 22.05 kHz | Fair | ~1.3 MB | Podcasts, spoken content |
| 44.1 kHz | Good | ~2.6 MB | General purpose, default CD quality |
| 48 kHz | Professional | ~2.8 MB | Music production, video soundtracks |

### Channel Options

- **Mono (1 channel)**: Single audio track, smaller files, suitable for voice and speech
- **Stereo (2 channels)**: Two audio tracks, larger files, required for music and multitrack content

### File Size Calculation

Approximate file size formula:
```
Size (MB) = (Duration (seconds) × Sample Rate (Hz) × Channels × Bit Depth (bytes)) / (1024 × 1024)
Size (MB) = (Duration × Sample Rate × Channels × 2) / 1,048,576
```

Example: 10 seconds, 44.1kHz, Mono, 16-bit
```
(10 × 44100 × 1 × 2) / 1,048,576 = ~0.84 MB
```

## Known Issues and Limitations

### Current Limitations

1. **Single Audio Device**: Cannot select among multiple audio devices (uses system default)
2. **No Audio Editing**: Cannot edit recordings post-capture (use external software like Audacity)
3. **No Real-Time Visualization**: No waveform display during recording
4. **No Audio Effects**: No built-in effects, filters, or mixing
5. **Directory Creation**: Only creates output directory if it doesn't exist; cannot create nested paths

### Potential Issues and Workarounds

**Issue**: "No audio input devices found" error
- **Cause**: Microphone disconnected or disabled
- **Solution**: Connect microphone, enable in system sound settings, restart application

**Issue**: Very slow startup on first run
- **Cause**: Packages being installed and compiled
- **Solution**: Normal behavior; subsequent launches are faster

**Issue**: Recording stutters or drops audio
- **Cause**: System under heavy load, insufficient resources
- **Solution**: Close other applications, increase blocksize in code (line 197)

**Issue**: WAV file corrupted or won't play
- **Cause**: Recording interrupted, disk full during save
- **Solution**: Ensure sufficient disk space, avoid forcefully closing application during recording

**Issue**: Cannot write to certain directories
- **Cause**: Insufficient permissions on output folder
- **Solution**: Choose folder with write permissions, run as administrator (if needed)

## Troubleshooting Guide

### Installation Issues

**Python not found after installation**
```
- Ensure "Add Python to PATH" was checked during Python setup
- Restart computer after Python installation
- Verify: Open Command Prompt and type 'python --version'
```

**pip not working**
```
- Update pip: python -m pip install --upgrade pip
- Try: python -m pip instead of just pip
- On Mac/Linux: Use python3 and pip3
```

**Dependencies won't install**
```bash
# Clear pip cache
python -m pip install --upgrade pip

# Install packages individually
python -m pip install sounddevice
python -m pip install numpy

# Check installation
python -c "import sounddevice; import numpy; print('Success')"
```

### Runtime Issues

**Tkinter not available (Linux)**
```bash
# Ubuntu/Debian
sudo apt install python3-tk python3-dev

# Fedora/RHEL
sudo dnf install python3-tkinter python3-devel
```

**Microphone permissions (Linux)**
```bash
# Add user to audio group
sudo usermod -a -G audio $USER

# Log out and back in, or reboot
```

**run.bat closes immediately (Windows)**
1. Open Command Prompt
2. Navigate to project folder: `cd path\to\Voice-Recorder`
3. Run manually: `python voice_recorder_gui.py`
4. Read error message carefully

### Output Issues

**File won't save**
- Check available disk space: `df -h` (Linux/Mac) or disk management (Windows)
- Verify write permissions on output folder
- Try saving to Documents or Downloads folder

**Recording quality poor**
- Increase sample rate to 44.1kHz or 48kHz
- Check microphone placement (too far from source)
- Reduce background noise in environment
- Ensure microphone levels are adequate

**Large file sizes**
- Reduce sample rate to 16kHz for speech
- Use mono instead of stereo
- Shorter recording duration

## Technical Details

### Audio Processing Pipeline

```
Microphone Input
    ↓
sounddevice InputStream (float32, blocksize=1024)
    ↓
Accumulate frames in list
    ↓
Concatenate numpy arrays
    ↓
Scale float32 [-1.0, 1.0] to int16 [-32768, 32767]
    ↓
Clip values to prevent overflow
    ↓
Convert to numpy int16 array
    ↓
wave.open() WAV file writer
    ↓
Write metadata (channels, samplerate, sample width)
    ↓
Write audio bytes
    ↓
Save to disk
```

### Threading Model

```
Main Thread (GUI)
├── Display UI
├── Handle button clicks
├── Update progress via root.after()
└── Handle window close

Recording Thread (Background)
├── Query audio device
├── Open audio stream
├── Read audio blocks in loop
├── Check stop_event
├── Process and save audio
└── Signal completion via root.after()
```

## Performance Considerations

- **CPU Usage**: Minimal during recording (mostly I/O bound)
- **Memory Usage**: ~1-2 MB per minute of recording (depends on channels and sample rate)
- **Disk I/O**: Sequential write, optimized by OS buffering
- **GUI Responsiveness**: Maintained through background threading
- **Maximum Recording Duration**: Limited by available disk space, not application

## Compatibility Matrix

| OS | Python | Status | Notes |
|---|--------|--------|-------|
| Windows 10/11 | 3.9+ | Fully Supported | Use run.bat for easiest setup |
| macOS 10.14+ | 3.9+ | Fully Supported | May need to allow microphone access |
| Ubuntu 20.04+ | 3.8+ | Fully Supported | Install python3-tk first |
| Debian 11+ | 3.9+ | Fully Supported | Install python3-tk first |
| Fedora 34+ | 3.9+ | Fully Supported | Install python3-tkinter first |

## Project Status

**Version**: 1.0
**Status**: Production Ready
**Purpose**: College educational project
**Maintenance**: As-is for educational use

## License

See the [LICENSE](LICENSE) file for licensing information.

## Contributing

Suggestions for improvements:
- Device selection from dropdown menu
- Real-time waveform display
- Audio visualization
- Multiple format support (MP3, OGG)
- Recording scheduling
- Batch recording operations
