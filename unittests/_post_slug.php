#!/usr/bin/env /usr/bin/php
<?php
/**
 * Converts a given string into a URL or filename-friendly slug.
 *
 * @param string $input_str       The string to be converted into a slug.
 * @param string $sep_char        The character to replace any non-alphanumeric characters. Default '-'.
 * @param bool   $preserve_case   If true, retains the original case of the string. Default false.
 * @param int    $max_len         Maximum length for the resulting string. If set, the string may be truncated. Default 0.
 *
 * @return string                 The resulting slug.
 *
 * @example
 * echo post_slug("Hello, World!");  
 * // Output: "hello-world"
 * echo post_slug("Hello, World!", "_", true);  
 * // Output: "Hello_World"
 * echo post_slug("A title, with Ŝtřãņġę cHaracters ()");
 * // Output: "a-title-with-strange-characters"
 * echo post_slug(" A title, with Ŝtřãņġę cHaracters ()", "_", true);
 * // Output: "A_title_with_strange_characters"
 *
 * @version 1.0.0
 */
function post_slug($input_str, $sep_char = "-", $preserve_case = false, $max_len = 0) {
  // Empty $sep_char not permitted
  if (empty($sep_char)) $sep_char = '-';

  // Kludges to increase cross-platform output similarity
  $input_str = str_replace('–', '-', $input_str);
  $input_str = str_replace(['½', '¼'], $sep_char, $input_str);
  $input_str = str_replace(' & ', ' and ', $input_str);
  $input_str = str_replace('ʾ', '', $input_str);

  // Remove all HTML entities
  $input_str = preg_replace('/&[^ \t]*;/', $sep_char, $input_str);

  // Force all characters in $input_str to ASCII (or closest representation)
  $input_str = iconv('UTF-8', 'ASCII//TRANSLIT', $input_str);

  // Remove quotes, apostrophes, and backticks
  $input_str = preg_replace("/[\"'`’´]/", '', $input_str);

  // Force to lowercase if not preserve_case
  if (!$preserve_case) $input_str = strtolower($input_str);

  // Replace all non alpha-numeric characters with $sep_char
  $input_str = preg_replace('/[^a-zA-Z0-9]+/', $sep_char, $input_str);

  // Remove consecutive and trailing occurrences of $sep_char
  $input_str = trim($input_str, $sep_char);

  // If max_len > 0, check for overlength string and truncate
  if ($max_len && strlen($input_str) > $max_len) {
    $input_str = substr($input_str, 0, $max_len);
    $last_sep_char_pos = strrpos($input_str, $sep_char);
    if ($last_sep_char_pos !== false) {
      $input_str = substr($input_str, 0, $last_sep_char_pos);
    }
  }

  return $input_str;
}

// Example usage
/*
echo post_slug("Hello, World!") . "\n";
echo post_slug("Hello, World!", "_", true) . "\n";
echo post_slug("A title, with Ŝtřãņġę cHaracters ()") . "\n";
echo post_slug(" A title, with Ŝtřãņġę cHaracters ()", "_", true) . "\n";
*/

// fin

# Check if the script is run from the command line
if (PHP_SAPI === "cli") {
  global $argc, $argv;
  if($argc > 1) {
    $string = $argv[1];
    $sep_char = isset($argv[2]) ? $argv[2] : "-";
    $preserve = isset($argv[3]) ? filter_var($argv[3], FILTER_VALIDATE_BOOLEAN) : false;
    $maxlen = isset($argv[4]) ? intval($argv[4]) : 0;
    echo post_slug($string, $sep_char, $preserve, $maxlen);
    echo "\n";
  }
}

