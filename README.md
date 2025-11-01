# CueTools

[![PyPI version](https://img.shields.io/pypi/v/cuetools )](https://pypi.org/project/cuetools/ )
[![License](https://img.shields.io/github/license/Olezhich/CueLogic )](https://github.com/Olezhich/CueLogic/blob/main/LICENSE )
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)  
[![Coverage Status](https://coveralls.io/repos/github/Olezhich/CueTools/badge.svg?branch=dev)](https://coveralls.io/github/Olezhich/CueTools?branch=dev)
[![Tests](https://github.com/Olezhich/CueTools/workflows/Tests/badge.svg )](https://github.com/Olezhich/CueTools/actions )

> **Lightweight CUE sheet toolkit for Python**  
Parsing **Cue Sheets** (`.cue` files) into `Pydantic` data models and validating fields\
Serialising data models into **Cue Sheets** (`.cue` files)


## Features

- Parse `.cue` files into structured Python objects
- Generate `.cue` file content from data
- Simple and intuitive API like `json` standard library
- Lightweight — no external dependencies other than `Pydantic`
- Supports Python 3.10+

## Cue Sheet specification

- Main cue sheet specification
[https://wiki.hydrogenaudio.org/index.php?title=Cue_sheet](https://wiki.hydrogenaudio.org/index.php?title=Cue_sheet)

- Additioonal ReplayGain specification
[https://wiki.hydrogenaudio.org/index.php?title=ReplayGain_1.0_specification](https://wiki.hydrogenaudio.org/index.php?title=ReplayGain_1.0_specification)

## QuickStart
### Installation of the library
#### Via pip

```bash
pip install cuetools
```

#### Via poetry
```bash
poetry add cuetools
```
### Using of the library
```python
import cuetools

cue_string = """
FILE "track01.flac" WAVE
  TRACK 01 AUDIO
    TITLE "Intro"
    PERFORMER "Artist"
    INDEX 01 00:00:00
"""

cue_sheet = cuetools.loads(cue_string) 
#cue_sheet is instance of AlbumData class with parsed cue_string

track = cue_sheet.tracks[0]
#track is instance of TrackData class with parsed track data

print(track.file)      # Result: track01.flac
print(track.title)     # Result: Intro
print(track.performer) # Result: Artist
