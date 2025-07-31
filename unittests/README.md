# post_slug Testing Suite

This directory contains the comprehensive testing suite for the post_slug multi-language slug generator library.

## Test Components

### 1. Cross-Language Validation (`validate_slug_scripts`)
The main validation script that ensures all four implementations (Python, JavaScript, PHP, Bash) produce identical output.

**Usage:**
```bash
./validate_slug_scripts datasets/headlines.txt
./validate_slug_scripts -q datasets/booktitles.txt  # Quiet mode (errors only)
./validate_slug_scripts datasets/products.txt 0 '-' 1  # With case preservation
```

### 2. Test Datasets

Located in the `datasets/` directory:

- **headlines.txt** - News headlines with currency symbols, punctuation, and special formatting
- **booktitles.txt** - Book titles with international characters and complex punctuation
- **products.txt** - E-commerce product names with technical specifications
- **edge_cases.txt** - Comprehensive edge cases including:
  - 255 character limit testing
  - HTML entity handling
  - Non-Latin scripts
  - Special characters and regex patterns
  - Empty and whitespace strings
  - Real-world problematic titles

### 3. Unit Tests

#### Python Unit Tests (`test_post_slug.py`)
Comprehensive unit tests using Python's unittest framework:
```bash
python test_post_slug.py
```

Tests include:
- 255 character input limit validation
- HTML entity replacement with separator
- Error handling and empty string returns
- Case preservation options
- Custom separator characters
- Real-world use cases

#### Focused Feature Tests (`test_focused.sh`)
Quick test of key new features:
```bash
./test_focused.sh
```

#### New Features Test (`test_new_features.sh`)
Comprehensive test of all new functionality:
```bash
./test_new_features.sh
```

## Testing New Features (v1.0.1)

### 1. Input Length Limit (255 characters)
All implementations now enforce a 255 character limit on input strings for filesystem compatibility:
```bash
# Test with over 255 chars
echo "$(printf 'a%.0s' {1..300})" | ./_post_slug.py -
# Output will be exactly 255 'a' characters
```

### 2. HTML Entity Handling
HTML entities are now consistently replaced with the separator character:
```bash
./_post_slug.py "Barnes &amp; Noble"
# Output: "barnes-noble"

./_post_slug.py "AT&amp;T &copy; 2024"
# Output: "at-t-2024"
```

### 3. Error Handling
All implementations return empty string on error:
```bash
# Non-Latin script
./_post_slug.py "Привет мир"
# Output: ""

# Only special characters
./_post_slug.py "!@#$%^&*()"
# Output: ""
```

### 4. Regex Escaping (JavaScript)
The JavaScript implementation now properly escapes regex special characters in separators:
```bash
./_post_slug.js "Test Case" "."
# Output: "test.case"

./_post_slug.js "Test Case" "+"
# Output: "test+case"
```

## Running All Tests

To run the complete test suite:
```bash
# 1. Run cross-language validation on all datasets
./validate_slug_scripts datasets/headlines.txt
./validate_slug_scripts datasets/booktitles.txt
./validate_slug_scripts datasets/products.txt
./validate_slug_scripts datasets/edge_cases.txt

# 2. Run Python unit tests
python test_post_slug.py

# 3. Run focused feature tests
./test_focused.sh
```

## Adding New Tests

To add new test cases:

1. **For edge cases**: Add lines to `datasets/edge_cases.txt`
2. **For unit tests**: Add test methods to `test_post_slug.py`
3. **For cross-language validation**: Add to appropriate dataset file

## Expected Behavior

All implementations should:
1. Produce identical output for the same input
2. Limit input to 255 characters
3. Replace HTML entities with separator character
4. Return empty string on errors
5. Support custom separators and case preservation

## Known Limitations

- Non-Latin scripts (Cyrillic, Chinese, Arabic) result in empty strings
- Some Unicode transliteration differences exist between implementations
- These are documented and expected behaviors