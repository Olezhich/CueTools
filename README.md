# CueTools

[![PyPI version](https://img.shields.io/pypi/v/cuetools )](https://pypi.org/project/cuetools/ )
[![License](https://img.shields.io/github/license/Olezhich/CueLogic )](https://github.com/Olezhich/CueLogic/blob/main/LICENSE )
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)  
[![Coverage Status](https://coveralls.io/repos/github/Olezhich/CueTools/badge.svg?branch=dev)](https://coveralls.io/github/Olezhich/CueTools?branch=dev)
[![Build Status](https://github.com/Olezhich/CueLogic/workflows/Run%20Tests%20on%20PR/badge.svg )](https://github.com/Olezhich/CueLogic/actions )

> **Lightweight CUE sheet toolkit for Python.**  
Parse and generate `.cue` files programmatically.

---

## ✨ Features

- Parse `.cue` files into structured Python objects
- Generate `.cue` file content from data
- Simple and intuitive API
- Lightweight — no external dependencies
- Supports Python 3.10+

---

## Cue Sheet specification

- Main cue sheet specification
[https://wiki.hydrogenaudio.org/index.php?title=Cue_sheet](https://wiki.hydrogenaudio.org/index.php?title=Cue_sheet)

- Additioonal ReplayGain specification
[https://wiki.hydrogenaudio.org/index.php?title=ReplayGain_1.0_specification](https://wiki.hydrogenaudio.org/index.php?title=ReplayGain_1.0_specification)

## 🚀 QuickStart
**Installation of the library**

```bash
pip install cuetools
```
**Using of the library**
```python
import cuetools

cue_string = """
FILE "track01.flac" WAVE
  TRACK 01 AUDIO
    TITLE "Intro"
    PERFORMER "Artist"
    INDEX 01 00:00:00
"""

cue_sheet = loads(cue_data) 
#cue_sheet is instance of AlbumData dataclass with parsed cue_data

track = cuesheet.tracks[0]
#track is instance of TrackData dataclass with parsed track data

print(track.link)      # Result: track01.wav
print(track.title)     # Result: Intro
print(track.performer) # Result: Artist