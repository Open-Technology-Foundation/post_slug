#!/usr/bin/env node

function post_slug(inputStr, repl = '-', preserveCase = false, maxLen = 0) {
  // Handle empty replacement character
  if (!repl) {
    repl = '-';
  }

  // Convert special characters to ASCII equivalent
  inputStr = inputStr.normalize('NFD').replace(/[\u0300-\u036f]/g, '');

  // Remove quotes and backticks
  inputStr = inputStr.replace(/[`'"]/g, '');

  // Optionally convert to lowercase
  if (!preserveCase) {
    inputStr = inputStr.toLowerCase();
  }

  // Replace all non-alphanumeric characters with {repl}
  inputStr = inputStr.replace(/[^a-zA-Z0-9]/g, repl);

  // Escape any special characters in {repl}
  const escapedRepl = repl.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

  // Replace all multiple occurrences of {repl} with a single {repl}
  const replPattern = new RegExp(`${escapedRepl}+`, 'g');
  inputStr = inputStr.replace(replPattern, repl);

  // Remove leading and trailing {repl}
  inputStr = inputStr.replace(new RegExp(`^${escapedRepl}|${escapedRepl}$`, 'g'), '');

  // Check maxLen
  if(maxLen>0) {
    if(inputStr.length > maxLen) {
      inputStr = inputStr.substr(0, maxLen);
      const lastSepCharPos = inputStr.lastIndexOf(escapedRepl);
      if (lastSepCharPos !== -1) {
        inputStr = inputStr.substr(0, lastSepCharPos);
      }
    }
  }

  return inputStr;
}

// Parse command-line arguments
const args = process.argv.slice(2);
if (args.length != 0) {
  const stringToSlugify = args[0];
  const separatorChar = args[1] || '-';
  const preserveCaseFlag = (args[2] === '1');
  const maxLen = parseInt(args[3]) || 0;
  if (stringToSlugify != '') {
    // Call the post_slug function and print the result
    const result = post_slug(stringToSlugify, separatorChar, preserveCaseFlag, maxLen);
    console.log(result);
  }
}
