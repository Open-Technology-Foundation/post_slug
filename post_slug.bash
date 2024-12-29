#!/bin/bash

post_slug() {
  shopt -s extglob
  local input_str="${1:-}" sep_char="${2:--}" 
  local -i preserve_case=${3:-0} max_len=${4:-0} stop_words=${5:-0}
	
  # Empty `sep_char` not permitted.
  [[ -z "$sep_char" ]] && sep_char='-'
  sep_char=${sep_char:0:1}

  # Kludges to increase cross platform output similarity.
  input_str=$(echo "$input_str" | sed -e 's/—/-/g' -e 's/â�¹/Rs/g' -e 's/�/-/g' \
                                      -e "s/½/$sep_char/g" -e "s/¼/$sep_char/g" \
                                      -e 's/ \& / and /g' -e 's/★/ /g' -e "s/\?/$sep_char/g")

  # Remove all HTML entities
  #input_str=$(echo "$input_str" | sed -e 's/&[^[:blank:]]*;/ /g')
	input_str="${input_str//&*;/ }"

  # Force all characters in `input_str` to ASCII (or closest representation).
  input_str=$(echo "$input_str" | iconv -f utf-8 -t ASCII//TRANSLIT)
  input_str=${input_str//\?/}

  # Remove quotes, apostrophes, and backticks.
  input_str="${input_str//[\`\'\"’´]}"

  # Optionally convert to lowercase.
  ((preserve_case)) || input_str="${input_str,,}"

#	((stop_words)) && {
#		>&2 declare -p input_str
#		input_str="$(stopwords "$input_str")"
#  }

  # Replace all non-alphanumeric characters with {sep_char}.
  #input_str=$(echo "$input_str" | sed -e "s/[^a-zA-Z0-9]/$sep_char/g")
	input_str=$(tr -c 'a-zA-Z0-9' "$sep_char" <<< "$input_str")

  # Replace all multiple occurrences of {sep_char} with a single {sep_char}.
  #input_str=$(echo "$input_str" | sed -e "s/$sep_char\{2,\}/$sep_char/g")
	while [[ "$input_str" == *"$sep_char"$sep_char* ]]; do
  	input_str="${input_str//"$sep_char"$sep_char/$sep_char}"
	done

  # Remove leading and trailing {sep_char}.
  input_str="${input_str#"${sep_char}"}"
  input_str="${input_str%"${sep_char}"}"

  if ((max_len)); then
    if (( ${#input_str} > max_len )); then
      input_str="${input_str:0:$max_len}"
      input_str="${input_str%"$sep_char"*}"
    fi
  fi
  echo -n "$input_str"
}
declare -fx post_slug

# Only run main if the script is being executed directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
	post_slug_usage() {
		cat <<-'EOT'
post_slug: Converts a given string into a URL or filename-friendly slug.

This script serves as a utility for string transformation into slugs suitable for 
URLs or filenames. It replaces specific characters, removes HTML entities, normalizes
to ASCII, removes quotes, and performs various other transformations.

Globals:
  None

Arguments:
  input_str: The string to convert.
  sep_char: Character to replace non-alphanumeric characters. Default '-'.
  preserve_case: Whether to preserve case. Default 0 (0=force lowercase).
  max_len: Maximum length of the output. Default 0 (0=no limit).
  stop_words: Execute stopwords on the input string. Default 0.

Returns:
  Transformed slug string.

Depends: 
  iconv

Example:
  post_slug 'Hello, World!'
  post_slug 'Hello, World!' '_' true
  post_slug 'A title, with Ŝtřãņġę cHaracters ()'
  	# Output: "a-title-with-strange-characters"
  post_slug ' A title, with Ŝtřãņġę cHaracters ()' "_" 1
  	# Output: "A_title_with_strange_characters"
  post_slug ' A title, with Ŝtřãņġę cHaracters ()' "_" 1 1 
  	# Output: "title_strange_characters"

EOT
		exit "${1:-0}"
	}

  set -euo pipefail
	[[ "${1:-}" == '-h' || "${1:-}" == '--help' ]] && post_slug_usage 0
  post_slug "$@"
else
  true
fi

#fin
