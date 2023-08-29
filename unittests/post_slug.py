#!/usr/bin/env python
"""
Function: post_slug(input_str: str, sep_char: str = "-", preserve_case: bool = False) -> str

The `post_slug` module provides a utility function for converting a given string into a URL or filename-friendly slug.

The function performs multiple transformations to ensure the resulting slug is readable and safe for use in URLs or filenames.

The function does this:
  - Forces all characters in `input_str` to ASCII (or closest representation).
  - Removes quotes, apostrophes, and backticks.
  - Forces to lowercase if not `preserve_case`.
  - Returns only valid alpha-numeric chars, replaces all other chars with `sep_char` char, removes all repetitions of `sep_char`, and strips `sep_char` from ends of string.

Function Parameters:
  - `input_str`: The string to be converted into a slug (required).
  - `sep_char`: The character to replace non-alphanumeric characters (optional; default '-').
  - `preserve_case`: Whether to retain the original case of the string (optional; default False).

Requires:
  Python 3.10 or higher.
  Modules `re` and `unicodedata`.

Example Usage:
  ```python
  from post_slug import post_slug
  print(post_slug("Hello, World!"))
  # Output: "hello-world"
  print(post_slug("Hello, World!", '_', True))
  # Output: "Hello_World"
  print(post_slug('A title, with  Ŝtřãņġę  cHaracters ()'))
  # Output: "a-title-with-strange-characters" 
  print(post_slug(' A title, with  Ŝtřãņġę  cHaracters ()', '_', True))
  # Output: "a_title_with_strange_characters"
  ```

"""
__version__ = '1.0.0'
import re
import unicodedata

def post_slug(input_str: str, sep_char: str = "-", preserve_case: bool = False, max_len:int = 0) -> str:
  """
  Converts a given string into a URL or filename-friendly slug.

  Args:
    input_str (str): The string to be converted into a slug.
    sep_char (str, optional): The character to replace any non-alphanumeric characters. Default '-'.
    preserve_case (bool, optional): If True, retains the original case of the string. Default False.

  Returns:
    str: The resulting slug.

  Example:
    print(post_slug("Hello, World!"))
    print(post_slug(' A title, with  Ŝtřãņġę  cHaracters ()', '_', True))

  """
  # Empty `sep_char` not permitted.
  if not sep_char: sep_char = '-'

  # Force all characters in `input_str` to ASCII (or closest representation).
  asciiized = unicodedata.normalize('NFKD', input_str).encode('ASCII', 'ignore').decode()
  # Remove quotes, apostrophes, and backticks.
  asciiized = re.sub(r"[\"'`]", '', asciiized)
  # Force to lowercase if not preserve_case.
  if not preserve_case:
    asciiized = asciiized.lower()
  # Return only valid alpha-numeric chars and the `sep_char` char, 
  # replacing all other chars with the `sep_char` char, 
  # then removing all repetitions of `sep_char` within the string, 
  # and stripping `sep_char` from ends of the string.
  asciiized = re.sub(r'[^a-zA-Z0-9]+', sep_char, asciiized).strip(sep_char)
  if max_len and len(asciiized) > max_len:
    asciiized = asciiized[0:max_len]
    last_sep_char_pos = asciiized.rfind(sep_char)
    if last_sep_char_pos != -1:
      asciiized = asciiized[0:last_sep_char_pos]
  return asciiized

if __name__ == '__main__':
  import sys

  # Check for command-line arguments
  if len(sys.argv) < 2:
    print("Usage: python post_slug.py 'string to slugify' [separator character] [preserve case] [max length]")
    sys.exit(1)

  # Parse command-line arguments
  string_to_slugify = sys.argv[1]
  separator_char = sys.argv[2] if len(sys.argv) > 2 else '-'
  preserve_case_flag = bool(int(sys.argv[3])) if len(sys.argv) > 3 else False
  max_len = int(sys.argv[4]) if len(sys.argv) > 4 else 0

  # Call the post_slug function and print the result
  result = post_slug(string_to_slugify, separator_char, preserve_case_flag, max_len=max_len)
  print(result)

#fin


