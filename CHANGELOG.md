# Changelog

All notable changes to `cuetools` will be documented in this file.  
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [1.0.2] - 2025-12-18

### Added
- py.typed that should allow MyPy to correctly analyse custom types.
- seconds property in the FrameTime.

### Fixed
- CHANGELOG versions diff link.

## [1.0.1] - 2025-11-30

### Added
- Support for some new REM keywords in parser.

### Fixed
- Metadata and URLs in `pyproject.toml`.
- Improved formatting and clarity in `CHANGELOG.md`, added older versions.
- Track index validation. Now, when INDEX 00 is greater than 0, everything works correctly.

## [1.0.0] - 2025-11-27

> **This release is not backward compatible with previous versions.**

### Added
- New CUE sheet parsing logic similar to Flex + Bison way (in functions `load`, `loads`).
- Structured data models using **Pydantic** (replacing previous `dataclass`-based approach).
- Built-in **field validation** according to the CUE sheet specification.
- Custom, human-readable exceptions: `CueParseError`, `CueValidationError`.
- Detailed error reporting with a visual indicator (`^`).

### Changed
- Replaced `dataclass` models with **Pydantic models** (`AlbumData`, `TrackData`, etc.).
- Renamed and restructured model fields for clarity and consistency.
- Completely rewritten parsing logic — more robust and specification-compliant.

### Removed
- Support for legacy dataclass-based output.
- Old parsing logic with limited error handling.
- functions `dump()` and `dumps()` that were in older versions have not yet been implemented.

### Breaking Changes
- **No backward compatibility**: code written for pre-1.0 versions will not work without updates.
- Model field names and structure have changed.
- Parsing errors now raise custom exceptions instead of generic ones.

## [0.1.5] - 2025-08-01

### Added
- New docs.

### Changed
- imported RemData model to cuetools.
- Refactored annotations.

## [0.1.4] - 2025-07-04

### Added
- Rem replay gain fields

## [0.1.3] - 2025-07-01

### Added
- Tests coverage

### Changed
- Update ci.
- Update README.

## [0.1.2] - 2025-06-30

### Changed
- Updated cd.
- Fixed README.

## [0.1.1] - 2025-06-30

### Added
- New `dump()` and `dumps()` functions.

### Changed
- Fixed annotations.
- Updated cd.

## [0.1.0] - 2025-06-28

### Added
- Base parsing logic.
- Functions `load()` and `loads()`.
- Dataclasses for data models.


[Unreleased]: https://github.com/Olezhich/CueTools/compare/v1.0.2...main
[1.0.2]: https://github.com/Olezhich/CueTools/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/Olezhich/CueTools/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/Olezhich/CueTools/compare/v0.1.5...v1.0.0
[0.1.5]: https://github.com/Olezhich/CueTools/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/Olezhich/CueTools/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/Olezhich/CueTools/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/Olezhich/CueTools/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/Olezhich/CueTools/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/Olezhich/CueTools/releases/tag/v0.1.0
