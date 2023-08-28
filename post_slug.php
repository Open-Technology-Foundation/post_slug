#!/usr/bin/php
<?php

if($argc>1) {
  $t=$argv[1];
  $repl=$argv[2];
  $preserve=$argv[3];
} else {
  $repl = '-';
  $t=('mdd/sfd=(*345&*_-00Æ)abc') ."\n";
  $preserve=false;
}

echo "orig:$t\n";
echo "slug:" . post_slug($t, $repl, $preserve) ."\n";



function post_slug($input_str, $repl='-', $preserve_case=false) {
  if(empty($repl)) $repl = '-';

  # Convert to ASCII and remove quotes, apostrophes, and backticks.
  $input_str = iconv('UTF-8', 'ASCII//TRANSLIT', $input_str);
  $input_str = str_replace(array("'", '"', '`'), '', $input_str);

  # Optionally convert to lowercase.
  if(!$preserve_case) $input_str = strtolower($input_str);

  # Replace all non-alphanumeric characters with {repl}.
  $input_str = preg_replace('/[^a-zA-Z0-9]/', $repl, $input_str);

  # Replace all multiple occurrences of {repl} with a single {repl}.
  $input_str = preg_replace('/'. preg_quote($repl, '/') . '+/', $repl, $input_str);

  # Remove leading and trailing {repl}.
  $input_str = trim($input_str, $repl);

  return $input_str;
}

#fin
