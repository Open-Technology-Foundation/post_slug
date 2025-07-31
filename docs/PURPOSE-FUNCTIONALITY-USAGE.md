# PURPOSE-FUNCTIONALITY-USAGE

## Purpose

**post_slug** is a multi-language slug generator library that solves the common problem of converting human-readable text into URL and filename-safe ASCII slugs. It ensures **consistent slug generation across Python, Bash, PHP, and JavaScript** implementations.

### Problem Solved
- Converts text with special characters, accents, and symbols into safe slugs
- Ensures identical output across different programming languages
- Handles international text through ASCII transliteration
- Provides production-ready solution for URLs, filenames, and identifiers

### Target Users
- Web developers building CMS, blogs, or e-commerce sites
- System administrators standardizing filename conventions
- Multi-language development teams needing consistent slug generation
- Content managers working with international content

## Key Functionality

### Core Features
1. **Multi-language Support**: Identical implementations in Python, Bash, PHP, and JavaScript
2. **9-Step Transformation Pipeline**:
   - HTML entity removal
   - ASCII transliteration (é→e, ñ→n, etc.)
   - Quote and special character removal
   - Configurable separator character
   - Optional case preservation
   - Length limiting with word-boundary truncation
3. **Batch Processing**: Utility for renaming multiple files
4. **Comprehensive Testing**: Cross-language validation framework

### Configuration Options
- `input_str`: Text to convert (required)
- `sep_char`: Separator character (default: `-`)
- `preserve_case`: Keep original case (default: false/0)
- `max_len`: Maximum length (default: 0/unlimited)

## Usage

### Basic Usage Examples

#### Python
```python
from post_slug import post_slug

# Basic usage
slug = post_slug("Hello, World!")
# Output: "hello-world"

# With underscore separator and case preservation
slug = post_slug("Product Name™", "_", True)
# Output: "Product_Name_TM"

# With length limit
slug = post_slug("Very Long Title That Needs Truncation", "-", False, 20)
# Output: "very-long-title-that"
```

#### Bash
```bash
source post_slug.bash

# Basic usage
post_slug "The Café's Menu"
# Output: "the-cafes-menu"

# Custom parameters
post_slug "Important Document.pdf" "_" 1 50
# Output: "Important_Document_pdf"
```

#### PHP
```php
require 'post_slug.php';

$slug = post_slug("L'École française");
// Output: "l-ecole-francaise"

$slug = post_slug("Product: High-Quality™", "_", true);
// Output: "Product_High_Quality_TM"
```

#### JavaScript
```javascript
const { post_slug } = require('./post_slug.js');

// Basic usage
const slug = post_slug("Breaking News!");
// Output: "breaking-news"

// With options
const slug = post_slug("New Feature (Beta)", "-", true, 15);
// Output: "New-Feature"
```

### Common Workflows

#### 1. Blog Post URLs
```python
title = "10 Tips for Better Sleep & Health!"
url_slug = post_slug(title)
# Result: "10-tips-for-better-sleep-health"
# Full URL: https://blog.com/posts/10-tips-for-better-sleep-health
```

#### 2. File Renaming
```bash
# Rename all files in directory to slug format
./slug-files -p --max-len 50 /path/to/documents/*.pdf
# "Annual Report 2023.pdf" → "annual-report-2023.pdf"
```

#### 3. Product Identifiers
```php
$product_name = "Samsung Galaxy S24 Ultra (256GB)";
$product_slug = post_slug($product_name, "-", false, 30);
// Result: "samsung-galaxy-s24-ultra"
```

#### 4. Cross-Language Validation
```bash
# Test slug consistency across all implementations
cd unittests
./validate_slug_scripts datasets/headlines.txt

# Test with specific parameters
./validate_slug_scripts datasets/booktitles.txt 127 '-' 0
```

## Requirements

### Language-Specific Requirements
- **Python**: ≥ 3.10 (uses built-in modules)
- **Bash**: ≥ 5.1 with `iconv` ≥ 2.3
- **PHP**: ≥ 8.0
- **JavaScript**: Node.js ≥ 12.2

### Installation
```bash
# Python package installation
pip install post_slug

# Or use directly from source
git clone https://github.com/Open-Technology-Foundation/post_slug.git
```

## Important Notes

### Consistency Guarantee
All four implementations produce identical slugs for the same input, making it safe to use different languages in the same project or during migrations.

### Character Handling
- **Supported**: Latin-based alphabets with diacritics (à, é, ñ, ü, etc.)
- **Limited Support**: Non-Latin scripts (Cyrillic, Chinese, Arabic) may produce empty strings
- **Special Characters**: All converted to separator or removed

### Example Transformations
```
"The Ŝtřãņġę (Inner) Life! of the \"Outsider\"" → "the-strange-inner-life-of-the-outsider"
"Café con Leche €3.50" → "cafe-con-leche-3-50"
"Product™ & Services®" → "product-tm-and-services-r"
"Hello___World!!!!" → "hello-world"
```

### Performance Considerations
- Multiple regex operations may impact performance on large datasets
- For bulk operations, use the `slug-files` utility which is optimized for batch processing

## Testing

The project includes comprehensive testing:
- Real-world test datasets (headlines, book titles, product names)
- Cross-language validation framework
- Automated consistency checking

Run tests with:
```bash
cd unittests
./validate_slug_scripts datasets/headlines.txt
```

This library provides a robust, tested solution for slug generation that works consistently across multiple programming languages, making it ideal for diverse development environments and migration scenarios.