#!/bin/bash

post_slug() {
  shopt -s extglob
  local input_str="${1:-}" repl="${2:--}" preserve_case="${3:-0}"

  # Convert to ASCII and remove quotes and apostrophes
  input_str=$(echo "$input_str" | iconv -f UTF-8 -t ASCII//TRANSLIT)
  input_str="${input_str//[\`\'\"]}"

  # Optionally convert to lowercase
  if [[ $preserve_case -eq 0 ]]; then
    input_str="${input_str,,}"
  fi

  # Replace all non-alphanumeric characters with {repl}
  input_str="${input_str//[^a-zA-Z0-9]/"$repl"}"

  # Replace all multiple occurrences of {repl} with a single {repl}
  while [[ $input_str == *"${repl}${repl}"* ]]; do
    input_str="${input_str//${repl}${repl}/"$repl"}"
  done

  # Remove leading and trailing {repl}
  input_str="${input_str#"${repl}"}"
  input_str="${input_str%"${repl}"}"

  echo -n "$input_str"
}

declare -fx post_slug
