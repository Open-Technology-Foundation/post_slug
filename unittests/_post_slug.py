#!/usr/bin/env /ai/scripts/.ai/bin/python
#!/usr/bin/env python
"""
post_slug Module
================

This module provides a utility function `post_slug` for converting a given string into a URL or filename-friendly slug.

The function performs multiple transformations to ensure the resulting slug is readable and safe for use in URLs or filenames. Specifically, it:

  - Replaces certain platform-specific characters with the separator character.
  - Removes all HTML entities.
  - Converts all characters to ASCII (or the closest representation).
  - Removes quotes, apostrophes, and backticks.
  - Converts the string to lowercase unless specified otherwise.
  - Retains only valid alphanumeric characters, replacing others with a separator character.
  - Optionally truncates the string to a maximum length, cutting off at the last separator character.

Parameters:
-----------
- `input_str` (str): The string to be converted into a slug.
- `sep_char` (str, optional): The character used to replace non-alphanumeric characters. Default is '-'.
- `preserve_case` (bool, optional): If True, retains the original case of the string. Default is False.
- `max_len` (int, optional): Maximum length for the resulting string. Default is 0, which means no limit.

Returns:
--------
- str: The resulting slug.

Example Usage:
--------------
```python
from post_slug import post_slug

print(post_slug("Hello, World!"))
# Output: "hello-world"

print(post_slug("Hello, World!", '_', True))
# Output: "Hello_World"

print(post_slug("A title, with Ŝtřãņġę cHaracters ()"))
# Output: "a-title-with-strange-characters"

print(post_slug(" A title, with Ŝtřãņġę cHaracters ()", "_", True))
# Output: "A_title_with_strange_characters"
```

Requires:
---------
- Python 3.10 or higher
- `re` and `unicodedata` modules

Version:
--------
1.0.0
"""
__version__ = '1.0.0'
import re
import unicodedata

"""
Kludge transliteration 
Create a translation table for single-character replacements
"""
translation_table = str.maketrans({
    '–': '-',
    '½': '-',
    '¼': '-',
    'ı': 'i',
    '•': 'o',
    'ł': 'l',
    '—': '-',
    '★': ' ',
    'ø': 'o',
    'Đ': 'D',
    'ð': 'd',
    'đ': 'd',
    '´': '',
    'Ł': 'L'
})
"""
Kludge Dictionary for multi-character replacements
"""
multi_char_replacements = {
    ' & ': ' and ',
    'œ': 'oe',
    '™': '-TM',
    'Œ': 'OE',
    'ß': 'ss',
    'æ': 'ae'
}

def post_slug(input_str: str, sep_char: str = "-", 
    preserve_case: bool = False, max_len:int = 0) -> str:
  """
  Convert a given string into a URL or filename-friendly slug.
  
  This function performs multiple transformations on the input string to create
  a slug that is both human-readable and safe for use in URLs or filenames.

  Parameters:
  ----------
  input_str : str
      The string to be converted into a slug.
  sep_char : str, optional
      The character used to replace any non-alphanumeric characters. Defaults to '-'.
  preserve_case : bool, optional
      If True, retains the original case of the string. Defaults to False.
  max_len : int, optional
      Maximum length for the resulting string. If set, the string may be truncated. Defaults to 0.

  Returns:
  -------
  str
      The resulting slug.

  Examples:
  --------
  >>> post_slug("Hello, World!")
  'hello-world'
  
  >>> post_slug("Hello, World!", "_", True)
  'Hello_World'
  
  >>> post_slug("A title, with Ŝtřãņġę cHaracters ()")
  'a-title-with-strange-characters'
  
  >>> post_slug(" A title, with Ŝtřãņġę cHaracters ()", "_", True)
  'A_title_with_strange_characters'
  
  Requires:
  --------
  Python 3.10 or higher.
  Modules `re` and `unicodedata`.

  Version:
  --------
  1.0.0
  """
  # Empty `sep_char` not permitted.
  if sep_char == '': sep_char = '-'

  # Kludges to increase cross platform output similiarity.
  """
  input_str = input_str.replace('–', '-')\
      .replace(' & ', ' and ')\
      .replace('½', sep_char)\
      .replace('¼', sep_char)\
      .replace('œ', 'oe')\
      .replace('™', '-TM')\
      .replace('ı', 'i')\
      .replace('•', 'o')\
      .replace('ł', 'l')\
      .replace('Œ', 'OE')\
      .replace('—', '-')\
      .replace('★', ' ')\
      .replace('ß', 'ss')\
      .replace('ø', 'o')\
      .replace('æ', 'ae')\
      .replace('Đ', 'D')\
      .replace('ð', 'd')\
      .replace('đ', 'd')\
      .replace('´', '')\
      .replace('Ł', 'L')
  """

  # Apply single-character replacements using str.translate()
  input_str = input_str.translate(translation_table)
  # Apply multi-character replacements
  for old, new in multi_char_replacements.items():
      input_str = input_str.replace(old, new)
  # Kludges end------------- ------------------------------------

  # Remove all HTML entities.
  input_str = re.sub(r'&[^ \t]*;', sep_char, input_str)
 
  # Force all characters in `input_str` to ASCII (or closest representation).
  input_str = unicodedata.normalize('NFKD', input_str).encode('ASCII', 'ignore').decode()

  # Remove quotes, apostrophes, and backticks.
  input_str = re.sub(r"[\"'`’´]", '', input_str)

  # Force to lowercase if not preserve_case.
  if not preserve_case:
    input_str = input_str.lower()

  # Return only valid alpha-numeric chars and the `sep_char` char, 
  # replacing all other chars with the `sep_char` char, 
  # then removing all repetitions of `sep_char` within the string, 
  # and stripping `sep_char` from ends of the string.
  input_str = re.sub(r'[^a-zA-Z0-9]+', sep_char, input_str).strip(sep_char)

  # If max_len > 0, then check for overlength string,
  # and truncate on last sep_char.
  if max_len and len(input_str) > max_len:
    input_str = input_str[0:max_len]
    last_sep_char_pos = input_str.rfind(sep_char)
    if last_sep_char_pos != -1:
      input_str = input_str[0:last_sep_char_pos]

  return input_str

#fin

if __name__ == '__main__':
  import sys

  # Check for command-line arguments
  if len(sys.argv) < 2:
    print('Usage: python post_slug.py string2slugify [separator character] [preserve case] [max length]')
    sys.exit(1)

  # Parse command-line arguments
  string_to_slugify = sys.argv[1]
  separator_char = sys.argv[2] if len(sys.argv) > 2 else '-'
  preserve_case_flag = bool(int(sys.argv[3])) if len(sys.argv) > 3 else False
  max_len = int(sys.argv[4]) if len(sys.argv) > 4 else 0

  # Call the post_slug function and print the result
  result = post_slug(string_to_slugify, separator_char, preserve_case_flag, max_len=max_len)
  print(result)

