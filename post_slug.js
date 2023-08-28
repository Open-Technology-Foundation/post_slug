function post_slug(inputStr, repl = '-', preserveCase = false) {
  // Handle empty replacement character
  if (!repl) {
    repl = '-';
  }

  // Convert special characters to ASCII equivalent (limited compared to iconv)
  // Note: JavaScript does not have a native equivalent for iconv
  inputStr = inputStr.normalize('NFD').replace(/[\u0300-\u036f]/g, '');

  // Remove quotes and backticks
  inputStr = inputStr.replace(/[`'"]/g, '');

  // Optionally convert to lowercase
  if (!preserveCase) {
    inputStr = inputStr.toLowerCase();
  }

  // Replace all non-alphanumeric characters with {repl}
  inputStr = inputStr.replace(/[^a-zA-Z0-9]/g, repl);

  // Replace all multiple occurrences of {repl} with a single {repl}
  const replPattern = new RegExp(`${repl}+`, 'g');
  inputStr = inputStr.replace(replPattern, repl);

  // Remove leading and trailing {repl}
  inputStr = inputStr.replace(new RegExp(`^${repl}|${repl}$`, 'g'), '');

  return inputStr;
}
