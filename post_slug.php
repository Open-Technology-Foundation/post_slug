<?php
function post_slug($input_str, $sep_char='-', $preserve_case=false, $max_len=0) {
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

  if ($max_len) {
    if (strlen($input_str) > $max_len) {
      # Trim the string to max_len
      $input_str = substr($input_str, 0, $max_len);
      # Find last occurrence of sep_char and truncate
      $last_sep_char_pos = strrpos($input_str, $sep_char);
      if ($last_sep_char_pos !== false)
          $input_str = substr($input_str, 0, $last_sep_char_pos);
    }
  }
  return $input_str;
}

#fin
