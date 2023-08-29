#!/usr/bin/php
<?php
function post_slug($input_str, $sep_char='-', $preserve_case=false, $maxlen=0) {
  if(empty($sep_char)) $sep_char = '-';

  # Convert to ASCII and remove quotes, apostrophes, and backticks.
  $input_str = iconv('UTF-8', 'ASCII//TRANSLIT', $input_str);
  $input_str = str_replace(array("'", '"', '`'), '', $input_str);

  # Optionally convert to lowercase.
  if(!$preserve_case) $input_str = strtolower($input_str);

  # Replace all non-alphanumeric characters with {sep_char}.
  $input_str = preg_replace('/[^a-zA-Z0-9]/', $sep_char, $input_str);

  # Replace all multiple occurrences of {sep_char} with a single {sep_char}.
  $input_str = preg_replace('/'. preg_quote($sep_char, '/') . '+/', $sep_char, $input_str);

  # Remove leading and trailing {sep_char}.
  $input_str = trim($input_str, $sep_char);

  if ($maxlen) {
    if (strlen($input_str) > $maxlen) {
      # Trim the string to maxlen
      $input_str = substr($input_str, 0, $maxlen);
      # Find last occurrence of sep_char and truncate
      $last_sep_char_pos = strrpos($input_str, $sep_char);
      if ($last_sep_char_pos !== false)
          $input_str = substr($input_str, 0, $last_sep_char_pos);
    }
  }

  return $input_str;
}

# Check if the script is run from the command line
if (PHP_SAPI === 'cli') {
  global $argc, $argv;
  if($argc > 1) {
    $string = $argv[1];
    $sep_char = isset($argv[2]) ? $argv[2] : '-';
    $preserve = isset($argv[3]) ? filter_var($argv[3], FILTER_VALIDATE_BOOLEAN) : false;
    $maxlen = isset($argv[4]) ? intval($argv[4]) : 0;
    echo post_slug($string, $sep_char, $preserve, $maxlen);
    echo "\n";
  }
}

#fin
