#!/usr/bin/env /usr/bin/bash
#!/bin/bash
#
# post_slug: Converts a given string into a URL or filename-friendly slug.
#
# This script serves as a utility for string transformation into slugs suitable for 
# URLs or filenames. It replaces specific characters, removes HTML entities, normalizes
# to ASCII, removes quotes, and performs various other transformations.
#
# Globals:
#   None
#
# Arguments:
#   input_str: The string to convert.
#   sep_char: Character to replace non-alphanumeric characters. Default '-'.
#   preserve_case: Whether to preserve case. Default 0 (0=force lowercase).
#   max_len: Maximum length of the output. Default 0 (0=no limit).
#
# Returns:
#   Transformed slug string.
#
# Depends: 
#   iconv
# 
# Example:
#   echo $(post_slug 'Hello, World!')
#   echo $(post_slug 'Hello, World!' '_' true)
#   echo $(post_slug 'A title, with Ŝtřãņġę cHaracters ()')
#   # Output: "a-title-with-strange-characters"
#   echo $(post_slug ' A title, with Ŝtřãņġę cHaracters ()' "_" 1)
#   # Output: "A_title_with_strange_characters"
# 
post_slug() {
  shopt -s extglob
  local input_str="${1:-}" sep_char="${2:--}" 
  local -i preserve_case=${3:-0} max_len=${4:-0}

  # Empty `sep_char` not permitted.
  [[ "$sep_char" == '' ]] && sep_char='-'

  # Kludges to increase cross platform output similiarity.
  input_str=${input_str//—/-}
  input_str=${input_str//½/"$sep_char"}
  input_str=${input_str//¼/"$sep_char"}
  input_str=${input_str// \& / and }
  input_str=${input_str//★/ }
  input_str=${input_str//\?/"$sep_char"}

  # Remove all HTML entities
  while [[ "$input_str" =~ \&[^[:blank:]]*\; ]]; do
    input_str=${input_str//${BASH_REMATCH[0]}/}
  done

  # Force all characters in `input_str` to ASCII (or closest representation).
  input_str=$(echo "$input_str" | iconv -f utf-8 -t ASCII//TRANSLIT)
  input_str=${input_str//\?/}

  # Remove quotes, apostrophes, and backticks.
  input_str="${input_str//[\`\'\"’´]}"

  # Optionally convert to lowercase.
  ((preserve_case)) || input_str="${input_str,,}"

  # Replace all non-alphanumeric characters with {sep_char}.
  input_str="${input_str//[^a-zA-Z0-9]/"$sep_char"}"

  # Replace all multiple occurrences of {sep_char} with a single {sep_char}.
  input_str=${input_str//+($sep_char)/$sep_char}

  # Remove leading and trailing {sep_char}.
  input_str="${input_str#"${sep_char}"}"
  input_str="${input_str%"${sep_char}"}"

  if ((max_len)); then
    if (( ${#input_str} > max_len )); then
      input_str="${input_str:0:$max_len}"
      input_str="${input_str%"${sep_char}"*}"
    fi
  fi
  echo -n "$input_str"
}
declare -fx post_slug

#fin

# If the script is being run directly, execute the function
if [[ "$0" != "-bash" && "$0" != "bash" ]]; then
  if [[ "$#" -eq 0 ]]; then
    echo "Usage: $(basename $0) "string to slugify" [separator character] [preserve case] [max length]"
    exit 1
  fi
  post_slug "$@"
  echo ""
fi

