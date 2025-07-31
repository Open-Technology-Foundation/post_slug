#!/usr/bin/env python3
"""
Unit tests for post_slug implementations
Tests new features: 255 char limit, HTML entities, error handling
"""

import unittest
import subprocess
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from post_slug import post_slug


class TestPostSlug(unittest.TestCase):
    """Test cases for post_slug function"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.implementations = {
            'py': os.path.join(self.test_dir, '_post_slug.py'),
            'js': os.path.join(self.test_dir, '_post_slug.js'),
            'bash': os.path.join(self.test_dir, '_post_slug.bash'),
            'php': os.path.join(self.test_dir, '_post_slug.php')
        }
    
    def run_implementation(self, impl, *args):
        """Run a specific implementation and return output"""
        cmd = [self.implementations[impl]] + [str(arg) for arg in args]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            return "TIMEOUT"
        except Exception as e:
            return f"ERROR: {e}"
    
    def test_all_implementations(self, input_str, sep_char='-', preserve_case=0, max_len=0):
        """Test all implementations return the same result"""
        results = {}
        for impl in self.implementations:
            results[impl] = self.run_implementation(impl, input_str, sep_char, preserve_case, max_len)
        
        # Check all results are the same
        unique_results = set(results.values())
        if len(unique_results) > 1:
            self.fail(f"Implementations differ for '{input_str}': {results}")
        
        return list(unique_results)[0]
    
    # Test 255 character limit
    def test_255_char_limit_exact(self):
        """Test string exactly 255 characters"""
        input_str = "1" * 257  # 257 chars
        result = self.test_all_implementations(input_str)
        self.assertEqual(len(result), 255, "Should truncate to 255 characters")
        self.assertEqual(result, "1" * 255)
    
    def test_255_char_limit_under(self):
        """Test string under 255 characters"""
        input_str = "test-string-under-limit"
        result = self.test_all_implementations(input_str)
        self.assertEqual(result, "test-string-under-limit")
    
    def test_255_char_limit_with_special_chars(self):
        """Test 255 limit with special characters"""
        input_str = "Test! String@ With# Special$ Chars% " * 20  # Long string
        result = self.test_all_implementations(input_str)
        self.assertLessEqual(len(result), 255)
        self.assertTrue(result.startswith("test-string-with-special-chars"))
    
    # Test HTML entity handling
    def test_html_entity_single(self):
        """Test single HTML entity"""
        result = self.test_all_implementations("Barnes &amp; Noble")
        self.assertEqual(result, "barnes-noble")
    
    def test_html_entity_multiple(self):
        """Test multiple HTML entities"""
        result = self.test_all_implementations("&lt;Test&gt; &amp; &quot;Example&quot;")
        self.assertEqual(result, "test-example")
    
    def test_html_entity_with_custom_separator(self):
        """Test HTML entities with custom separator"""
        result = self.test_all_implementations("A &amp; B", "_")
        self.assertEqual(result, "a_b")
    
    # Test error handling
    def test_empty_string(self):
        """Test empty string input"""
        result = self.test_all_implementations("")
        self.assertEqual(result, "")
    
    def test_only_spaces(self):
        """Test string with only spaces"""
        result = self.test_all_implementations("   ")
        self.assertEqual(result, "")
    
    def test_only_special_chars(self):
        """Test string with only special characters"""
        result = self.test_all_implementations("!@#$%^&*()")
        self.assertEqual(result, "")
    
    def test_non_latin_script(self):
        """Test non-Latin script (should return empty)"""
        result = self.test_all_implementations("Привет мир")
        self.assertEqual(result, "")
    
    # Test case preservation
    def test_case_preservation_off(self):
        """Test default lowercase conversion"""
        result = self.test_all_implementations("iPhone iPad", "-", 0)
        self.assertEqual(result, "iphone-ipad")
    
    def test_case_preservation_on(self):
        """Test case preservation"""
        result = self.test_all_implementations("iPhone iPad", "-", 1)
        self.assertEqual(result, "iPhone-iPad")
    
    # Test custom separators
    def test_separator_underscore(self):
        """Test underscore separator"""
        result = self.test_all_implementations("Test Case", "_")
        self.assertEqual(result, "test_case")
    
    def test_separator_plus(self):
        """Test plus separator"""
        result = self.test_all_implementations("Test Case", "+")
        self.assertEqual(result, "test+case")
    
    def test_separator_period(self):
        """Test period separator"""
        result = self.test_all_implementations("Test Case", ".")
        self.assertEqual(result, "test.case")
    
    # Test real-world cases
    def test_real_world_covid(self):
        """Test COVID-19 title"""
        result = self.test_all_implementations("COVID-19: A Global Pandemic")
        self.assertEqual(result, "covid-19-a-global-pandemic")
    
    def test_real_world_currency(self):
        """Test currency symbols"""
        result = self.test_all_implementations("Price: $100.50 or €85.99")
        self.assertEqual(result, "price-100-50-or-eur85-99")
    
    def test_real_world_email(self):
        """Test email address"""
        result = self.test_all_implementations("Contact: user@example.com")
        self.assertEqual(result, "contact-user-example-com")
    
    def test_real_world_url(self):
        """Test URL"""
        result = self.test_all_implementations("Visit https://example.com/page")
        self.assertEqual(result, "visit-https-example-com-page")
    
    # Test edge cases
    def test_consecutive_separators(self):
        """Test multiple consecutive separators are collapsed"""
        result = self.test_all_implementations("Test   Multiple   Spaces")
        self.assertEqual(result, "test-multiple-spaces")
    
    def test_leading_trailing_special(self):
        """Test leading/trailing special characters"""
        result = self.test_all_implementations("!!!Test!!!")
        self.assertEqual(result, "test")
    
    def test_mixed_quotes(self):
        """Test various quote types"""
        result = self.test_all_implementations('"Smart quotes" and 'curly apostrophes'')
        self.assertEqual(result, "smart-quotes-and-curly-apostrophes")


class TestPostSlugPython(unittest.TestCase):
    """Test Python implementation directly"""
    
    def test_python_direct_import(self):
        """Test direct Python import works"""
        result = post_slug("Test String")
        self.assertEqual(result, "test-string")
    
    def test_python_error_handling(self):
        """Test Python error handling"""
        # This should not raise an exception
        result = post_slug(None)
        self.assertEqual(result, "")


if __name__ == '__main__':
    # Run with verbose output
    unittest.main(verbosity=2)