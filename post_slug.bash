#!/bin/bash
# post_slug - Convert strings into URL/filename-friendly ASCII slugs
# Transliterates to ASCII, removes special chars, normalizes separators
# Returns empty string on error for safe handling

post_slug() {
  local -- input_str="${1:-}" sep_char="${2:--}"
  local -i preserve_case=${3:-0} max_len=${4:-0}

  ((${#input_str})) || { echo ''; return 0; }

  [[ -n "$sep_char" ]] || sep_char='-'
  sep_char=${sep_char:0:1}
  ((${#input_str} < 256)) || input_str="${input_str:0:255}"

  # Kludges to increase cross platform output similarity.
  input_str="${input_str//—/-}"
  input_str="${input_str//â�¹/Rs}"
  input_str="${input_str//�/-}"
  input_str="${input_str//½/$sep_char}"
  input_str="${input_str//¼/$sep_char}"
  input_str="${input_str// & / and }"
  input_str="${input_str//★/ }"
  input_str="${input_str//[?]/$sep_char}"
  input_str="${input_str//€/EUR}"
  input_str="${input_str//©/C}"
  input_str="${input_str//®/R}"
  input_str="${input_str//™/-TM}"

  # Remove HTML entities
  [[ "$input_str" != *'&'*';'* ]] || \
    input_str=$(sed "s/&[^[:space:]]*;/$sep_char/g" <<< "$input_str")

  # Force to ASCII via iconv
  input_str=$(iconv -f utf-8 -t ASCII//TRANSLIT <<< "$input_str" 2>/dev/null) || return
  input_str=${input_str//\?/}
  input_str="${input_str//[\`\'\"’´]}"

  ((preserve_case)) || input_str="${input_str,,}"
  input_str="${input_str//[^a-zA-Z0-9]/$sep_char}"

  while [[ "$input_str" == *"$sep_char"$sep_char* ]]; do
    input_str="${input_str//"$sep_char"$sep_char/$sep_char}"
  done
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

[[ "${BASH_SOURCE[0]}" == "${0}" ]] || return 0

set -euo pipefail

show_help() {
  cat <<-'EOT'
post_slug - Convert strings into URL/filename-friendly ASCII slugs

Usage: post_slug <input_str> [sep_char] [preserve_case] [max_len]

Arguments:
  input_str      String to convert (max 255 chars)
  sep_char       Separator character (default: '-')
  preserve_case  0=lowercase, 1=preserve (default: 0)
  max_len        Max output length, 0=unlimited (default: 0)

Examples:
  post_slug 'Hello, World!'           # hello-world
  post_slug 'Hello, World!' '_' 1     # Hello_World
  post_slug 'Long title here' '-' 0 8 # long

EOT
}

[[ "${1:-}" == '-h' || "${1:-}" == '--help' ]] && { show_help; exit 0; }

post_slug "$@"
#fin
