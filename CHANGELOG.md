# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2025-01-31

### Added
- 255 character input limit for filesystem safety
- Comprehensive error handling with try-catch blocks
- Cross-language consistency for Euro (€), copyright (©), and registered (®) symbols
- HTML entity handling standardization (replaced with separator character)
- Regex escaping fix in JavaScript implementation
- Comprehensive test suite with edge cases dataset
- Security audit documentation (AUDIT-EVALUATE.md)
- Purpose and functionality documentation
- Claude AI integration guidelines (CLAUDE.md)

### Changed
- HTML entities now consistently replaced with separator character across all languages
- Improved bash implementation to prevent duplicate output
- Updated all version numbers to 1.0.1
- Enhanced documentation and README

### Fixed
- Bash validation script duplicate output bug (line 149)
- JavaScript regex escaping for special separator characters
- HTML entity pattern in Bash (was too greedy)
- Version mismatch in Python __version__

### Security
- Added 255 character input limit to prevent DoS attacks
- Improved input validation across all implementations
- Added comprehensive error handling to prevent crashes

## [1.0.0] - 2023-09-01

### Added
- Initial release with Python, JavaScript, PHP, and Bash implementations
- Cross-language slug generation with consistent output
- Configurable separator character
- Optional case preservation
- Maximum length truncation
- Character transliteration with kludge tables
- Validation test framework
- Test datasets (headlines, booktitles, products)
- Batch file renaming utility (slug-files)
- Comprehensive documentation

### Features
- URL and filename-safe slug generation
- ASCII-only output
- Removal of HTML entities
- Quote and apostrophe removal
- Leading/trailing separator cleanup
- Unicode to ASCII transliteration