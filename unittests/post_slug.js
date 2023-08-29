#!/usr/bin/env node

/**
 * Function: post_slug(inputStr: string, sepChar: string = "-", preserveCase: boolean = false, maxLen: number = 0) -> string
 * 
 * The `post_slug` function provides a utility for converting a given string into a URL or filename-friendly slug.
 * 
 * - Forces all characters in `inputStr` to ASCII (or closest representation).
 * - Removes quotes, apostrophes, and backticks.
 * - Forces to lowercase if not `preserveCase`.
 * - Replaces all non-alphanumeric characters with `sepChar`.
 * - Removes all repetitions of `sepChar`.
 * - Strips `sepChar` from ends of string.
 * 
 * @param {string} inputStr - The string to be converted into a slug.
 * @param {string} sepChar - The character to replace non-alphanumeric characters.
 * @param {boolean} preserveCase - Whether to retain the original case of the string.
 * @param {number} maxLen - The maximum length for the slug.
 * @returns {string} - The resulting slug.
 */

function post_slug(inputStr, sepChar = "-", preserveCase = false, maxLen = 0) {
  // Handle empty replacement character
  if (!sepChar) sepChar = '-';
  
  // Convert to ASCII and remove quotes and backticks
  inputStr = inputStr.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  inputStr = inputStr.replace(/[`'"]/g, "");
  
  // Optionally convert to lowercase
  if (!preserveCase) inputStr = inputStr.toLowerCase();
  
  // Replace all non-alphanumeric characters with sepChar
  inputStr = inputStr.replace(/[^a-zA-Z0-9]/g, sepChar);
  
  // Escape special characters in sepChar
  const escapedSepChar = sepChar.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  
  // Replace all multiple occurrences of sepChar with a single sepChar
  const sepCharPattern = new RegExp(`${escapedSepChar}+`, "g");
  inputStr = inputStr.replace(sepCharPattern, sepChar);
  
  // Remove leading and trailing sepChar
  inputStr = inputStr.replace(new RegExp(`^${escapedSepChar}|${escapedSepChar}$`, "g"), "");
  
  // Implement the maxLen feature
  if (maxLen && inputStr.length > maxLen) {
    inputStr = inputStr.substring(0, maxLen);
    const lastSepCharPos = inputStr.lastIndexOf(sepChar);
    if (lastSepCharPos !== -1) {
      inputStr = inputStr.substring(0, lastSepCharPos);
    }
  }
  
  return inputStr;
}

// Command-line interface
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 0) {
    const stringToSlugify = args[0];
    const separatorChar = args[1] || "-";
    const preserveCaseFlag = args[2] === "1";
    const maxLen = parseInt(args[3]) || 0;
    console.log(post_slug(stringToSlugify, separatorChar, preserveCaseFlag, maxLen));
  }
}
