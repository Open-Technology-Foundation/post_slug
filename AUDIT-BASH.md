# AUDIT-BASH: post_slug.bash

**Date:** 2026-04-17
**Auditor:** Leet (Claude Code, Opus 4.7)
**Target:** `/ai/scripts/lib/str/post_slug/post_slug.bash`
**Standard:** Bash Coding Standard (BCS), Bash 5.2+
**File statistics:** 85 lines, 2 functions (`post_slug`, `show_help`), dual-purpose library

---

## Executive Summary

**Overall Health Score: 7.0 / 10**

A compact, well-scoped slug utility. Core algorithm is readable and correct. Dual-purpose (source/exec) pattern follows BCS0106 with minor deviations. One ShellCheck warning, several BCS structural gaps, one suspected data-corruption issue in the kludge table (mojibake bytes), and one latent security consideration from `declare -i` on untrusted input.

Strengths:
- Dual-purpose source fence at line 58 is correct.
- `((preserve_case)) || ...` pattern at line 39 is BCS0208-compliant.
- `#fin` end marker present (BCS0100.13).
- Safe empty-input early exit at line 10.
- Input truncation to 255 chars (line 14) limits attack surface.

### Top Critical Issues
1. **Kludge table contains mojibake / replacement characters** (lines 18-19). Likely source-file corruption.
2. **`declare -i` on caller-supplied arguments** (line 8) — arithmetic context is code-execution-capable in bash; untrusted callers can trigger side effects.
3. **No `shopt -s inherit_errexit`** when `set -euo pipefail` is enabled (line 60). Subshells do not inherit `errexit`.

### Quick Wins
- Replace `sed` (line 32) with parameter expansion (fixes SC2001).
- Explicit `return 1` on line 35 instead of bare `return`.
- Add `VERSION` constant (project has `VERSION` file; library should expose it).
- Add `shopt -s inherit_errexit` after `set -euo pipefail`.
- Fix file permissions: `chmod 0755 post_slug.bash` (current `0075` has no owner-read).

### Long-term Recommendations
- Introduce `_post_slug_validate_int()` helper to sanitize numeric args before `declare -i`.
- Replace mojibake-byte kludges with explicit Unicode code-point forms (e.g. `$'\u20b9'` for ₹).
- Consider a single-pass `sed`/`tr` pipeline or a lookup associative array instead of 12 sequential `${var//a/b}` substitutions.

### ShellCheck Results
- **1 warning:** SC2001 (style), line 32 — `sed` substitution replaceable by parameter expansion.

### BCS Compliance
Approx. **72%**. Dual-purpose script exemptions apply to several BCS0100 items. See findings below.

---

## Findings by Severity

### HIGH

#### H1. Mojibake / replacement-character bytes in kludge table
- **Severity:** High
- **Location:** `post_slug.bash:18-19`
- **BCS:** BCS1202 (comment intent), BCS1005 (input validation)
- **Description:** Line 18 substitutes `â�¹` and line 19 substitutes `�` — the `�` glyph is the Unicode replacement character (U+FFFD), produced when a decoder hits invalid UTF-8. `â�¹` looks like UTF-8 mojibake of `₹` (U+20B9 Indian Rupee Sign) decoded as Latin-1. The source file itself contains broken bytes.
- **Impact:** The kludges will never match actual Rupee input (real `₹` is `0xe2 0x82 0xb9`, not the mojibake sequence stored). Behaviour is silently wrong. Also, saving a file containing U+FFFD is a strong smell that the editor mangled the source.
- **Recommendation:**
  ```bash
  # Use explicit code points — survives re-saves in any editor.
  input_str="${input_str//$'\u20b9'/Rs}"    # ₹ Indian Rupee
  input_str="${input_str//$'\ufffd'/-}"     # U+FFFD replacement char
  ```
  Audit all other kludge lines (17, 20-28) by regenerating them from explicit code points.

#### H2. `declare -i` on caller-supplied arguments enables arithmetic-context code paths
- **Severity:** High
- **Location:** `post_slug.bash:8`
- **BCS:** BCS1005 (input validation), BCS1004 (command injection)
- **Description:** `local -i preserve_case=${3:-0} max_len=${4:-0}` forces arithmetic evaluation of `$3` and `$4`. Bash arithmetic context evaluates identifiers as variable names recursively and can index arrays. An attacker-controlled caller passing e.g. `"a[$(cmd)]"` triggers `cmd`. Library is invoked from PHP/Python/shell wrappers, so trust boundary is non-obvious.
- **Impact:** Command execution through a function that looks like pure string manipulation. Medium likelihood (caller must be compromised), high blast radius (runs under caller's privileges).
- **Recommendation:**
  ```bash
  local -- pc_raw="${3:-0}" ml_raw="${4:-0}"
  [[ $pc_raw =~ ^[0-9]+$ ]] || pc_raw=0
  [[ $ml_raw =~ ^[0-9]+$ ]] || ml_raw=0
  local -i preserve_case=$pc_raw max_len=$ml_raw
  ```

### MEDIUM

#### M1. Missing `shopt -s inherit_errexit`
- **Severity:** Medium
- **Location:** `post_slug.bash:60` (after `set -euo pipefail`)
- **BCS:** BCS0100.5
- **Description:** Without `inherit_errexit`, command substitutions (`$(...)`) do not propagate `set -e`. Line 32 and 35 use command substitution; failures in the subshell pipeline may be masked.
- **Recommendation:**
  ```bash
  set -euo pipefail
  shopt -s inherit_errexit
  ```

#### M2. Bare `return` after `iconv` failure
- **Severity:** Medium
- **Location:** `post_slug.bash:35`
- **BCS:** BCS0602 (explicit exit codes)
- **Description:** `iconv ... || return` returns the last command's exit code. While this works, it's opaque; caller cannot distinguish transliteration failure from other paths.
- **Recommendation:** `iconv -f utf-8 -t ASCII//TRANSLIT <<<"$input_str" 2>/dev/null || { echo ''; return 10; }` (ERR_TYPE = wrong format).

#### M3. ShellCheck SC2001 — `sed` call replaceable by parameter expansion
- **Severity:** Medium
- **Location:** `post_slug.bash:32`
- **BCS:** Performance (Section 14); ShellCheck compulsory (Section 2)
- **Description:** `sed "s/&[^[:space:]]*;/$sep_char/g" <<<"$input_str"` spawns a subprocess per call.
- **Recommendation:** Parameter-expansion + extglob avoids the fork:
  ```bash
  shopt -s extglob
  input_str="${input_str//&*([!  ]);/$sep_char}"
  ```
  Note: trade-off — extglob pattern is slightly less readable; bench before committing. If kept, SC2001 can be suppressed with `# shellcheck disable=SC2001 # readability over micro-opt`.

#### M4. No `VERSION` constant exposed
- **Severity:** Medium
- **Location:** `post_slug.bash` (global scope)
- **BCS:** BCS0100.6
- **Description:** Sibling `VERSION` file, `pyproject.toml`, and `_version.py` all carry a version; the bash module does not. CLAUDE.md lists the bash module as a version-sync target.
- **Recommendation:**
  ```bash
  declare -r POST_SLUG_VERSION='1.0.2'   # Keep in sync via update_version.sh
  ```
  Update `update_version.sh` to touch this line.

#### M5. File permissions `0075` — owner cannot read
- **Severity:** Medium
- **Location:** filesystem (`ls -la`)
- **BCS:** BCS1001 (permission hygiene)
- **Description:** Mode `----rwxr-x` means the owner has no read/write bit; only group+other can execute/read. Unusual and likely a mistake. Not SUID/SGID so not a direct security finding, but it breaks `source post_slug.bash` when the owner is not in the file's group.
- **Recommendation:** `chmod 0755 post_slug.bash`.

### LOW

#### L1. Redundant `$` inside parameter expansion
- **Severity:** Low
- **Location:** `post_slug.bash:50`
- **BCS:** BCS0207
- **Description:** `${input_str:0:$max_len}` — the `$max_len` inside a parameter-expansion length position is an arithmetic context already; the `$` is unnecessary.
- **Recommendation:** `input_str="${input_str:0:max_len}"`.

#### L2. Double-separator collapse via loop is O(n²) worst-case
- **Severity:** Low
- **Location:** `post_slug.bash:42-44`
- **BCS:** Performance (Section 14)
- **Description:** The `while *sepsep* ...` loop walks the string on every iteration. For long inputs with many consecutive separators this is quadratic.
- **Recommendation:** Single pass with extglob:
  ```bash
  shopt -s extglob
  input_str="${input_str//+($sep_char)/$sep_char}"
  ```

#### L3. `[[ "$input_str" != *'&'*';'* ]] || ...` — OR-of-NOT idiom is hard to read
- **Severity:** Low
- **Location:** `post_slug.bash:31`
- **BCS:** BCS1202 (comments/clarity)
- **Description:** The `|| \<continuation>` guards an HTML-entity strip. The double-negative pattern reads awkwardly.
- **Recommendation:** Flip to positive form:
  ```bash
  if [[ $input_str == *'&'*';'* ]]; then
    input_str="${input_str//&*([!  ]);/$sep_char}"
  fi
  ```

#### L4. `echo ''` vs `printf` / empty
- **Severity:** Low
- **Location:** `post_slug.bash:10, 54`
- **BCS:** BCS0701 (I/O conventions)
- **Description:** Line 10 uses `echo ''` for empty output (emits newline). Line 54 uses `echo -n` (no newline). Inconsistent; callers get different behaviours on empty vs non-empty input.
- **Recommendation:** Use `printf '%s' ''` and `printf '%s' "$input_str"` for consistency. If a trailing newline is desired, use `printf '%s\n'` in both places.

#### L5. `-h`/`--help` check uses `${1:-}` under `set -u` but bypasses the parser
- **Severity:** Low
- **Location:** `post_slug.bash:82`
- **BCS:** BCS0801 (argument parsing pattern)
- **Description:** Ad-hoc `-h`/`--help` check instead of the `while (($#)); do case "$1" in` pattern. For a 2-option tool this is fine, but BCS prefers the canonical loop. Also, if `$1` is `-h`, flow jumps to `show_help` then `exit 0` — OK, but `post_slug "$@"` would run with `-h` as the string input otherwise (correctly produces slug `h`).
- **Recommendation:** Acceptable as-is for a tiny CLI; note in code. Alternative — drop the shortcut and call `post_slug "$@"` only after a case-loop.

#### L6. No `shellcheck` directive at top of file
- **Severity:** Low
- **Location:** `post_slug.bash:1-5`
- **BCS:** BCS0100.2
- **Description:** The file has shebang + description but no `# shellcheck shell=bash` or `source-path` directives. Not strictly required, but improves static-analysis of sourced consumers.
- **Recommendation:** Add `# shellcheck shell=bash` on line 2.

#### L7. `${input_str//[\`\'\"’´]}` — implicit empty replacement
- **Severity:** Low
- **Location:** `post_slug.bash:37`
- **BCS:** BCS1202 (clarity)
- **Description:** Works (bash treats missing `/repl` as empty) but is less explicit than `${var//pattern/}`.
- **Recommendation:** `input_str="${input_str//[\`\'\"’´]/}"` — trailing `/` signals intent.

#### L8. Kludge set replaces `½` and `¼` with separator
- **Severity:** Low
- **Location:** `post_slug.bash:20-21`
- **BCS:** Domain correctness
- **Description:** `½` → `-` loses information. Other implementations in the project (py/js/php) may treat fractions differently; cross-language parity is the project's stated goal.
- **Recommendation:** Audit `post_slug.py`/`.js`/`.php` for the same transform and align. Candidate: `½` → `1-2`, `¼` → `1-4`. Verify with `unittests/validate_slug_scripts datasets/edge_cases.txt`.

### INFO

- **I1.** Function order is top-down (`post_slug` before `show_help`). BCS0401 prefers bottom-up but the script has only one utility function so impact is nil.
- **I2.** No `main()` function. Script is 85 lines — well under the BCS0108 200-line threshold. Correct to omit.
- **I3.** `declare -fx post_slug` (line 56) exports the function. Useful if callers `bash -c`. Not strictly needed for pure `source`. Acceptable.
- **I4.** `sep_char=${sep_char:0:1}` (line 13) silently truncates multi-char separators. Document this in the help text, which currently says only "Separator character".

---

## BCS Section Compliance Matrix

| Section | Status | Notes |
|---|---|---|
| BCS0100 Script Structure | Partial | Missing `shopt inherit_errexit`, no VERSION constant. `#fin` present. |
| BCS0200 Variables | Good | `local --` / `local -i` used correctly; H2 flags untrusted `-i`. |
| BCS0300 Strings/Quoting | Good | Consistent single/double quoting. |
| BCS0400 Functions | Good | Naming, scope, `declare -fx` correct. |
| BCS0500 Control Flow | Good | `[[ ]]`, `(( ))`, `${var//}` patterns throughout. |
| BCS0600 Error Handling | Partial | Bare `return` (M2); no `die()` helper (not needed at this size). |
| BCS0700 I/O | Partial | L4 echo/printf inconsistency. |
| BCS0800 CLI | Partial | Ad-hoc help handling (L5) vs canonical case-loop. |
| BCS0900 File Ops | N/A | No file operations in core function. |
| BCS1000 Security | Partial | H2 `declare -i` on untrusted input. |
| BCS1100 Concurrency | N/A | None used. |
| BCS1200 Style | Good | 2-space indent, naming, comments reasonable. |

---

## Tool Output Summary

### ShellCheck (`shellcheck -x post_slug.bash`)
```
SC2001 (style) line 32: See if you can use ${variable//search/replace} instead.
```
Total: 1 warning, 0 errors.

### bcscheck
Successful run on 2026-04-18 via `bcscheck --model claude-code:thorough -e max post_slug.bash` (365s elapsed, claude-code backend). Result: **1 ERROR, 4 WARN**, exit 1.

| BCS Code | Tier | Severity | Line(s) | Description |
|---|---|---|---|---|
| BCS0101 | core | ERROR | 60 | Missing `shopt -s inherit_errexit` after `set -euo pipefail` |
| BCS0103 | recommended | WARN | 60–61 | No VERSION/SCRIPT_NAME metadata declared |
| BCS0207 | style | WARN | 58 | Unnecessary braces: `"${0}"` → `"$0"` |
| BCS0408 | recommended | WARN | 35 | `iconv` dependency not checked with `command -v` |
| BCS0806 | recommended | WARN | 82 | Missing `-V/--version` option support |

#### Cross-reference with manual findings

| bcscheck finding | Manual audit match |
|---|---|
| BCS0101 (inherit_errexit) | **M1** — same finding. |
| BCS0103 (VERSION metadata) | **M4** — same finding, manual was narrower (VERSION only). |
| BCS0207 (`"${0}"` braces) | *New — not in manual audit.* Add to fix list. |
| BCS0408 (iconv check) | *New — not in manual audit.* Add to fix list. |
| BCS0806 (`-V/--version`) | *New as a graded finding.* Manual audit's patch script already added `-V/--version` handling; promote to explicit L9. |

#### New findings to add to section above

**L9. Unnecessary braces on `${0}`** — `post_slug.bash:58`, BCS0207. Change `[[ "${BASH_SOURCE[0]}" == "${0}" ]]` → `[[ ${BASH_SOURCE[0]} == "$0" ]]`.

**M6. `iconv` dependency not guarded by `command -v`** — `post_slug.bash:35`, BCS0408. `iconv` is not a POSIX/coreutils tool. Add guard in script mode (line 60+) or at first invocation:
```bash
command -v iconv >/dev/null || { printf '%s' ''; return 18; }
```

**M7. Missing `-V/--version`** — `post_slug.bash:82`, BCS0806. Add alongside help handler:
```bash
case "${1:-}" in
  -h|--help)    show_help; exit 0 ;;
  -V|--version) printf '%s %s\n' post_slug "$POST_SLUG_VERSION"; exit 0 ;;
esac
```

#### Earlier failed attempts (for posterity)

Before the successful `claude-code:thorough` run, six other backend/model combinations failed — `qwen3.5:14b` not installed, cloud models locked behind subscription/timeouts, local 8–9B models either looped in `thinking` with empty output or produced generic prose without BCS codes.

---

## Suggested Patch (consolidated)

```bash
#!/bin/bash
# shellcheck shell=bash
# post_slug - Convert strings into URL/filename-friendly ASCII slugs
# Transliterates to ASCII, removes special chars, normalizes separators
# Returns empty string on error for safe handling

declare -r POST_SLUG_VERSION='1.0.2'

post_slug() {
  local -- input_str="${1:-}" sep_char="${2:--}"
  local -- pc_raw="${3:-0}" ml_raw="${4:-0}"
  [[ $pc_raw =~ ^[0-9]+$ ]] || pc_raw=0
  [[ $ml_raw =~ ^[0-9]+$ ]] || ml_raw=0
  local -i preserve_case=$pc_raw max_len=$ml_raw

  ((${#input_str})) || { printf '%s' ''; return 0; }

  [[ -n $sep_char ]] || sep_char='-'
  sep_char=${sep_char:0:1}
  ((${#input_str} < 256)) || input_str="${input_str:0:255}"

  # Kludges — use explicit code points to survive editor re-saves.
  input_str="${input_str//—/-}"
  input_str="${input_str//$'\u20b9'/Rs}"   # ₹ Rupee
  input_str="${input_str//$'\ufffd'/-}"    # U+FFFD replacement
  input_str="${input_str//½/$sep_char}"
  input_str="${input_str//¼/$sep_char}"
  input_str="${input_str// & / and }"
  input_str="${input_str//★/ }"
  input_str="${input_str//[?]/$sep_char}"
  input_str="${input_str//€/EUR}"
  input_str="${input_str//©/C}"
  input_str="${input_str//®/R}"
  input_str="${input_str//™/-TM}"

  # Strip HTML entities without fork.
  shopt -s extglob
  [[ $input_str != *'&'*';'* ]] || \
    input_str="${input_str//&*([! $'\t '])\;/$sep_char}"

  input_str=$(iconv -f utf-8 -t ASCII//TRANSLIT <<<"$input_str" 2>/dev/null) \
    || { printf '%s' ''; return 10; }
  input_str=${input_str//\?/}
  input_str="${input_str//[\`\'\"’´]/}"

  ((preserve_case)) || input_str="${input_str,,}"
  input_str="${input_str//[^a-zA-Z0-9]/$sep_char}"

  # Collapse runs of sep_char in one pass.
  input_str="${input_str//+($sep_char)/$sep_char}"
  input_str="${input_str#"$sep_char"}"
  input_str="${input_str%"$sep_char"}"

  if ((max_len)) && ((${#input_str} > max_len)); then
    input_str="${input_str:0:max_len}"
    input_str="${input_str%"$sep_char"*}"
  fi
  printf '%s' "$input_str"
}
declare -fx post_slug

[[ ${BASH_SOURCE[0]} == "${0}" ]] || return 0

set -euo pipefail
shopt -s inherit_errexit

show_help() {
  cat <<-'EOT'
	post_slug - Convert strings into URL/filename-friendly ASCII slugs

	Usage: post_slug <input_str> [sep_char] [preserve_case] [max_len]

	Arguments:
	  input_str      String to convert (max 255 chars)
	  sep_char       Separator char, first byte only (default: '-')
	  preserve_case  0=lowercase, 1=preserve (default: 0)
	  max_len        Max output length, 0=unlimited (default: 0)
	EOT
}

case "${1:-}" in
  -h|--help) show_help; exit 0 ;;
  -V|--version) printf '%s %s\n' post_slug "$POST_SLUG_VERSION"; exit 0 ;;
esac

post_slug "$@"
#fin
```

Validate after patching:
```bash
cd /ai/scripts/lib/str/post_slug/unittests
./validate_slug_scripts datasets/headlines.txt
./validate_slug_scripts datasets/booktitles.txt
./validate_slug_scripts datasets/edge_cases.txt
shellcheck -x ../post_slug.bash
bcscheck ../post_slug.bash
```

#fin
