# Slug Generator Functions for Python/Bash/PHP/Javascript

## Overview

The `post_slug` functions are designed to convert any given text into a URL- or filename- friendly ASCII slug.  Although the primary use case is to generate slugs for headlines, article titles, and book titles, it is also suitable for generating slugs for URLs and filenames generally. This package offers implementations of `post_slug` in Python, Bash, PHP, and JavaScript.

The `post_slug` functions perform multiple transformations on the input string to create a slug that is both human-readable and safe for use in URLs or filenames, and that is _consistent between each implementation_.

This package contains `post_slug` function modules for Python, Bash, PHP, and Javascript:

	post_slug.py
	post_slug.bash
	post_slug.php
	post_slug.js

Every language function takes the same following parameters:

	"string" [separator char='-'] [preserve case=0] [max length=0]

Optional parameters, when used, must be applied consistently across the project or platform.

All function modules generate slugs using the same methodology, thus ensuring an extremely high degree of consistency. For example:

	The Ŝtřãņġę (Inner) Life! of the "Outsider"

Using default parameters, with any of the modules, becomes:

	the-strange-inner-life-of-the-outsider

Note: Some non-Latin character sets may not be able to be transliterated at all, such as Cyrillic:

	нее Стгаиеде (Іииег) Ліғе! оғ тне 'Оутсідег'

Be aware that this would cause an empty string to be returned.

Many non-Latin characters cannot be transliterated into the ASCII set, and can only be ignored.


### Manual Transliterations (Kludges)

The Python and Javascript function modules use `	unicodedata.normalize('NFKD', ...)` for transliteration, whereas Bash and PHP use `iconv('UTF-8', 'ASCII//TRANSLIT', ...)`.

Manual Transliterations ("kludges") are required to account for the very small number of inconsistencies in translation that might appear.

These kludges greatly increase cross-language slug similiarity for most typical input.

Python and Javascript in particular require their different kludge tables, both single- and multi- character.  Bash and PHP only require a few kludges.

If required, the kludge tables can be edited in the source.   Please generate pull requests to add to these translitation tables where necessary.

The bottom line is that these modules are not 100% accurate in situations where Non-Latin text is used, embedded or encountered. However, depending on the input used, this is statistically insignificant using real world data in situations where these modules would be typically used.

### Validating Slug Consistency (`validate_slug_scripts`)

In the unittests subdirectory, there is a script `/validate_slug_scripts`, which is used to test slug consistency between the modules on any test data.

	Usage: validate_slug_scripts [-q] [textfile [max_len [seps [cases]]]]

	Note: all parameters are positional.

	-q         	If specified, only report errors, 
				do not display each validation test.
	textfile   	Any text file; required
	max_len    	Maximum length of slug; default 0 (0=unlimited)
	seps       	Separator chars, delimited with ',', eg, '-,_,+'
	cases      	Cases to check, can be 0, 1, or '0,1' (1=preserve case)

	Modules to be tested are (py bash php js)
	Separator chars to be used are (_-)

When run, `validate_slug_scripts` generates standalone command-line scripts for each of the languages, utilizing the source of each of the modules in this package.  These standalone scripts are prefaced with '\_' and the execute permission is set.

```.../post_slug/unittests$ ls
	datasets         _post_slug.js   _post_slug.py
	_post_slug.bash  _post_slug.php  validate_slug_scripts
```

The command-line __Bash__ \_scripts in the `unittests` directory may be used for testing, and even production, but keep in mind that they are regenerated from module sources whenever `validate_slug_scripts` is executed.

```bash
./_post_slug.php "After Buddhism: Rethinking the Dharma for a Secular Age"
# Outputs:after-buddhism-rethinking-the-dharma-for-a-secular-age
./_post_slug.bash "After Buddhism: Rethinking the Dharma for a Secular Age"
# Outputs:after-buddhism-rethinking-the-dharma-for-a-secular-age
./_post_slug.js "After Buddhism: Rethinking the Dharma for a Secular Age"
# Outputs:after-buddhism-rethinking-the-dharma-for-a-secular-age
./_post_slug.py "After Buddhism: Rethinking the Dharma for a Secular Age"
# Outputs:after-buddhism-rethinking-the-dharma-for-a-secular-age
```

The `unittests/datasets` directory contains test data files.

## Requirements

### Python:
	- Python >= 3.10
	- module `unicodedata`

### Bash:
    - Bash >= 5.1
    - package `iconv` >= 2.3

### PHP:
    - PHP >= 8.0 

### Javascript:
	- node >= 12.2


## Usage

### Function Parameters

Each `post_slug` module takes four parameters: the string you want to convert, and optionally, the separator character (default '-'), the flag to preserve alphacase (default 0), and the maximum length of the returned string (default 0=unlimited).

	`input_str` : str
      The string to be converted into a slug.

  	`sep_char` : str, optional
      The character used to replace any non-alphanumeric characters. Defaults to '-'.

  	`preserve_case` : bool, optional
      If True|1, retains the original case of the string. Defaults to False|0.

  	`max_len` : int, optional
      Maximum length for the resulting string. If set, the string may be truncated at the last `sep_char`. Defaults to 0 (unlimited).

### Examples

```python
from post_slug import post_slug

# Basic usage, default options; '_' as sep_char, not preserving case:
print(post_slug("Hello, World! ... it's nice to see you. .. from time 2 time ;)...."))  
# Outputs: "hello-world-its-nice-to-see-you-from-time-2-time"

# Specifying '_' as sep_char, preserving case:
print(post_slug('A title, but embedded with these  (Ŝtřãņġę)  CHARacters... !^_^! ', '_', True))
# Outputs: "A_title_but_embedded_with_these_Strange_CHARacters"

# Specifying '_' as sep_char, not preserving case:
print(post_slug("Über die Universitäts-Philosophie  — Arthur Schopenhauer, 1851", '_'))
# Outputs: "uber_die_universitats_philosophie_arthur_schopenhauer_1851"

```

```bash
source post_slug.bash

# Basic usage, default options; '_' as sep_char, not preserving case:
echo $(post_slug "Hello, World! ... it's nice to see you. .. from time 2 time ;)....")
# Outputs: "hello-world-its-nice-to-see-you-from-time-2-time"

# Specifying '_' as sep_character, preserving case:
echo $(post_slug 'A title, but embedded with these  (Ŝtřãņġę)  CHARacters... !^_^! ' '_' 1)
# Outputs: "A_title_but_embedded_with_these_Strange_CHARacters"

# Specifying '_' as sep_char, not preserving case:
echo $(post_slug "Über die Universitäts-Philosophie  — Arthur Schopenhauer, 1851" '_')
# Outputs: "uber_die_universitats_philosophie_arthur_schopenhauer_1851"

```


## Contributing

Feel free to submit pull requests or open issues to improve the modules in this package.

https://github.com/Open-Technology-Foundation/post_slug.git

