#!/bin/bash
# Function: post_slug
# Desc    : Produce a URL-friendly slug string.
#         :
#         : String is lowercased, and non-ASCII chars replaced with 
#         : ASCII-equivalent.
#         :
#         : All non-alnum chars are replaced with {sep_char} (default '-')
#         :
#         : Multiple occurances of {sep_char} are reduced to one, and 
#         : leading and trailing {sep_char} chars removed.
#         :
# Synopsis: myslug=$(post_slug "str" ["sep_char"])
#         :   replstr   is optional, defaults to '-'
#         :
# Example : post_slug 'A title, with  Ŝŧřãņġę  cHaracters ()'
#         : # ^ returns "a-title-with-strange-characters" 
#         :
#         : post_slug ' A title, with  Ŝŧřãņġę  cHaracters ()" '_'
#         : # ^ returns: "a_title_with_strange_characters"
#         :
# Depends : iconv

post_slug() {
  shopt -s extglob
  local input_str="${1:-}" sep_char="${2:--}" preserve_case="${3:-0}"

  # Convert to ASCII and remove quotes, apostrophes and backticks.
  input_str=$(echo "$input_str" | iconv -f UTF-8 -t ASCII//TRANSLIT)
  input_str="${input_str//[\`\'\"]}"

  # Optionally convert to lowercase.
  if [[ $preserve_case -eq 0 ]]; then
    input_str="${input_str,,}"
  fi

  # Replace all non-alphanumeric characters with {sep_char}.
  input_str="${input_str//[^a-zA-Z0-9]/"$sep_char"}"

  # Replace all multiple occurrences of {sep_char} with a single {sep_char}.
  while [[ $input_str == *"${sep_char}${sep_char}"* ]]; do
    input_str="${input_str//${sep_char}${sep_char}/"$sep_char"}"
  done

  # Remove leading and trailing {sep_char}.
  input_str="${input_str#"${sep_char}"}"
  input_str="${input_str%"${sep_char}"}"

  echo -n "$input_str"
}

declare -fx post_slug
