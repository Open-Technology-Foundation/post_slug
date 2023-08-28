# Post Slug Python Module

## Overview

The `post_slug` Python module provides a utility function to convert any given string into a URL or filename-friendly slug.

This package always contains *equivalent functions* for Bash, PHP, and Javascript:

	post_slug.bash
	post_slug.php
	post_slug.js

## Requirements

- Python 3.10 or higher
- `re` and `unicodedata` modules

## Installation

Simply download the `post_slug.py` file and import it into your Python project. 

For Bash, PHP and Javascript usage, the equivalent function in `post_slug.bash`, `post_slug.php` or `post_slug.js`

## Usage

Import the function and pass the string you want to convert as the first argument. Optionally, you can also specify the separator character (def. '-') and whether to preserve the original string case.

### Example

```python
from post_slug import post_slug

# Basic usage
print(post_slug("Hello, World! ... it's nice to see you. .. from time 2 time ;)...."))  
# Output: "hello-world-its-nice-to-see-you-from-time-2-time"

# Specifying a replacement character and preserving case
print(post_slug('A title, but embedded with these  (Ŝtřãņġę)  CHARacters... ^_^!! ', '_', True))
# Output: "A_title_but_embedded_with_these_Strange_CHARacters"
```

## Function Parameters

- `input_str`: The string to be converted into a slug (required).
- `sep_char`: The character to replace non-alphanumeric characters (optional; default '-').
- `preserve_case`: Whether to retain the original case of the string (optional; default False).

## Contributing

Feel free to submit pull requests or open issues to improve this module and associated other language clones of this module.

https://github.com/Open-Technology-Foundation/post_slug.git



