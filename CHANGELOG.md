# Changelog

All notable changes to `cuetools` will be documented in this file.  
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

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

[Unreleased]: https://github.com/Olezhich/CueTools/compare/v1.0.0...main
[1.0.0]: https://github.com/Olezhich/CueTools/compare/v0.1.5...v1.0.0
[0.1.5]: https://github.com/Olezhich/CueTools/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/Olezhich/CueTools/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/Olezhich/CueTools/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/Olezhich/CueTools/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/Olezhich/CueTools/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/Olezhich/CueTools/releases/tag/v0.1.0
