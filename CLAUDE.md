# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a multi-language slug generator library that provides consistent URL/filename-friendly ASCII slugs across Python, Bash, PHP, and JavaScript implementations. The main purpose is to convert text (like article titles, book titles, headlines) into safe slugs for URLs or filenames.

## Commands

### Build & Distribution
```bash
# Build Python package
python -m build

# The built package will be in dist/post_slug-*.tar.gz
```

### Testing
```bash
# Run cross-language validation tests
cd unittests
./validate_slug_scripts datasets/headlines.txt
./validate_slug_scripts datasets/booktitles.txt
./validate_slug_scripts datasets/products.txt

# Test with specific parameters
./validate_slug_scripts datasets/headlines.txt 0 '-' 1  # preserve case
./validate_slug_scripts datasets/booktitles.txt 127 '-' 0  # max length 127
./validate_slug_scripts -q datasets/products.txt  # quiet mode (errors only)
```

### Running Individual Modules
```bash
# Python
python post_slug.py "Your Text Here"

# Bash
source post_slug.bash
post_slug "Your Text Here"

# PHP
php -r 'require "post_slug.php"; echo post_slug("Your Text Here") . "\n";'

# JavaScript
node -e 'const {post_slug} = require("./post_slug.js"); console.log(post_slug("Your Text Here"));'
```

## Architecture

### Core Components
1. **Module Files** (`post_slug.py`, `post_slug.bash`, `post_slug.php`, `post_slug.js`)
   - Each implements the same slug generation algorithm
   - All take the same parameters: `input_str`, `sep_char='-'`, `preserve_case=0`, `max_len=0`
   - Use language-specific transliteration methods with manual kludge tables for consistency

2. **Testing Framework** (`unittests/validate_slug_scripts`)
   - Generates standalone command-line wrappers (`_post_slug.*`) for each language
   - Validates slug consistency across all implementations
   - Uses test datasets in `unittests/datasets/`

### Key Implementation Details

The slug generation process follows these steps in order:
1. Language-specific character replacement (kludges)
2. HTML entity removal
3. Transliteration to ASCII
4. Quote/apostrophe/backtick removal
5. Optional lowercase conversion
6. Non-alphanumeric character replacement with separator
7. Multiple separator consolidation
8. Leading/trailing separator removal
9. Optional truncation at last separator

### Transliteration Methods
- **Python/JavaScript**: Use `unicodedata.normalize('NFKD', ...)`
- **Bash/PHP**: Use `iconv('UTF-8', 'ASCII//TRANSLIT')`
- Manual kludge tables compensate for transliteration differences between languages

## Important Notes

- When modifying any module, ensure changes are propagated to all language implementations
- Always run `validate_slug_scripts` after changes to verify cross-language consistency
- The `temp/` directory contains test files and should not be modified
- Generated test scripts (`_post_slug.*`) in `unittests/` are regenerated on each validation run
- Non-Latin characters (e.g., Cyrillic) may result in empty strings as they cannot be transliterated to ASCII