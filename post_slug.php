<?php
/**
 * Converts a given string into a URL or filename-friendly slug.
 * 
 * The function performs multiple transformations:
 * - Limits input to 255 characters to ensure filesystem compatibility
 * - Replaces HTML entities with the separator character
 * - Converts all characters to ASCII (or closest representation)
 * - Removes quotes, apostrophes, and backticks
 * - Converts to lowercase unless preserve_case is true
 * - Replaces non-alphanumeric characters with separator
 * - Removes consecutive separators
 * - Returns empty string on error for safe failure handling
 *
 * @param string $input_str       The string to be converted into a slug. Automatically truncated to 255 characters.
 * @param string $sep_char        The character to replace any non-alphanumeric characters. Default '-'.
 * @param bool   $preserve_case   If true, retains the original case of the string. Default false.
 * @param int    $max_len         Maximum length for the resulting string. If set, the string may be truncated. Default 0 (no limit beyond 255 char input limit).
 *
 * @return string                 The resulting slug, or empty string on error.
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
 * @version 1.0.1
 * 
 * @changelog
 * 1.0.1 - Added 255 character input limit, standardized HTML entity handling,
 *         added error handling with try-catch and iconv error checking.
 * 1.0.0 - Initial release
 */
function post_slug($input_str, $sep_char = "-", $preserve_case = false, $max_len = 0) {
  try {
    // Empty $sep_char not permitted
    if ($sep_char == '') $sep_char = '-';
    $sep_char = $sep_char[0];
    
    // Limit input to 255 characters
    if (strlen($input_str) > 255) {
      $input_str = substr($input_str, 0, 255);
    }

    // Kludges to increase cross-platform output similarity
  $kludge_replacements = [
    '–' => '-', 'â�¹' => 'Rs', '½' => $sep_char, '¼' => $sep_char, '�' => $sep_char,
    ' & ' => ' and ', 'ʾ' => '',
    '€' => 'EUR',  // Euro symbol - already handled by iconv but added for consistency
    '©' => 'C',    // Copyright symbol
    '®' => 'R',    // Registered trademark
    '™' => '-TM'   // Trademark symbol
  ];
  $input_str = str_replace(array_keys($kludge_replacements), array_values($kludge_replacements), $input_str);

  // Remove all HTML entities
  $input_str = preg_replace('/&[^ \t]*;/', $sep_char, $input_str);

  // Force all characters in $input_str to ASCII (or closest representation)
  $input_str = @iconv('UTF-8', 'ASCII//TRANSLIT', $input_str);
  if ($input_str === false) {
    return '';
  }

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
  } catch (Exception $e) {
    return '';
  }
}

// Example usage
/*
echo post_slug("Hello, World!") . "\n";
echo post_slug("Hello, World!", "_", true) . "\n";
echo post_slug("A title, with Ŝtřãņġę cHaracters ()") . "\n";
echo post_slug(" A title, with Ŝtřãņġę cHaracters ()", "_", true) . "\n";
*/

// fin