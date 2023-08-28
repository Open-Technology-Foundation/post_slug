# Post Slug Python Module

## Overview

The `post_slug` Python module provides a utility function to convert any given string into a URL or filename-friendly slug.

## Requirements

- Python 3.10 or higher
- `re` and `unicodedata` modules

## Installation

Simply download the `post_slug.py` file and import it into your Python project.

## Usage

Import the function and pass the string you want to convert as the first argument. Optionally, you can also specify a replacement character and whether to preserve the original string case.

### Example

```python
from post_slug import post_slug

# Basic usage
print(post_slug("Hello, World!"))  
# Output: "hello-world"

# Specifying a replacement character and preserving case
print(post_slug('A title, with  Ŝtřãņġę  cHaracters ()', '_', True))
# Output: "A_title_with_strange_characters"
```

## Function Parameters

- `input_str`: The string to be converted into a slug (required).
- `repl`: The character to replace non-alphanumeric characters (optional; default '-').
- `preserve_case`: Whether to retain the original case of the string (optional; default False).

## Contributing

Feel free to submit pull requests or open issues to improve the module.

