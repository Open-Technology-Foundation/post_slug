#!/usr/bin/env /usr/bin/node
//#!/usr/bin/env node
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

/**
 * Transliteration Kludges
 * Create translation table for single-character replacements.
 */
const translationTable = {
  '–': '-',
  '½': '-',
  '¼': '-',
  'ı': 'i',
  '•': 'o',
  'ł': 'l',
  '—': '-',
  '★': ' ',
  'ø': 'o',
  'Đ': 'D',
  'ð': 'd',
  'đ': 'd',
  'Ł': 'L',
  'ʼ': '',
  '´': '',
  'ʾ': ''
};

/**
 * Kludge Dictionary for multi-character replacements.
 */
const multiCharReplacements = {
  ' & ': ' and ',
  'œ': 'oe',
  '™': '-TM',
  'Œ': 'OE',
  'ß': 'ss',
  'æ': 'ae',
  'â�¹': 'Rs',
  '�': '-',
};

function post_slug(inputStr, sepChar = "-", preserveCase = false, maxLen = 0) {
  // Handle empty replacement character
  if (sepChar == '') sepChar = '-';
 
  // Kludges to increase cross platform slug similiarity.
    /**
     * Apply single-character replacements
     */
  for (const [oldChar, newChar] of Object.entries(translationTable)) {
    const regex = new RegExp(oldChar, 'g');
    inputStr = inputStr.replace(regex, newChar);
  }
    /**
     * Apply multi-character replacements.
     */
  for (const [oldStr, newStr] of Object.entries(multiCharReplacements)) {
    const regex = new RegExp(oldStr, 'g');
    inputStr = inputStr.replace(regex, newStr);
  }

  // Remove all HTML entities.
  inputStr = inputStr.replace(/&[^ \t]*;/g, '');
  
  // Force all characters in `input_str` to ASCII (or closest representation).
  inputStr = inputStr.normalize("NFKD").replace(/[\u0300-\u036f]/g, "");

  // Remove quotes, apostrophes, and backticks.
  inputStr = inputStr.replace(/[`'"’´]/g, "");
  
  // Optionally convert to lowercase
  if (!preserveCase) inputStr = inputStr.toLowerCase();
  
  // Replace all non-alphanumeric characters with sepChar
  inputStr = inputStr.replace(/[^a-zA-Z0-9]/g, sepChar);
  
  // Escape special characters in sepChar
  const escapedSepChar = sepChar.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  
  /* Return only valid alpha-numeric chars and the `sep_char` char, 
     replacing all other chars with the `sep_char` char, 
     then removing all repetitions of `sep_char` within the string, 
     and stripping `sep_char` from ends of the string. */
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

//fin

// Command-line interface
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 0) {
    const stringToSlugify = args[0];
    const separatorChar = args[1] || '-';
    const preserveCaseFlag = args[2] === '1';
    const maxLen = parseInt(args[3]) || 0;
    console.log(post_slug(stringToSlugify, separatorChar, preserveCaseFlag, maxLen));
  }
}

