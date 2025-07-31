# Contributing to post_slug

Thank you for your interest in contributing to post_slug! This document provides guidelines and instructions for contributing to the project.

## 🤝 Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## 🔄 Development Process

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/post_slug.git
cd post_slug
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 3. Make Changes

#### Important: Cross-Language Consistency

**All changes must be implemented across all four language implementations:**
- Python (`post_slug.py`)
- JavaScript (`post_slug.js`)
- PHP (`post_slug.php`)
- Bash (`post_slug.bash`)

### 4. Test Your Changes

```bash
cd unittests
./validate_slug_scripts datasets/headlines.txt
./validate_slug_scripts datasets/booktitles.txt
./validate_slug_scripts datasets/edge_cases.txt

# Run Python unit tests
python test_post_slug.py
```

### 5. Commit Your Changes

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
git commit -m "feat: add support for emoji transliteration"
git commit -m "fix: correct HTML entity pattern in bash"
git commit -m "docs: update installation instructions"
```

## 📋 Contribution Guidelines

### Code Style

1. **Python**: Follow PEP 8
2. **JavaScript**: Use consistent formatting (2 spaces, semicolons)
3. **PHP**: Follow PSR-12
4. **Bash**: Use shellcheck and follow Google's style guide

### Adding Kludges

When adding character transliterations:

1. Add to the kludge table in each implementation
2. Document why the kludge is needed
3. Add test cases to `edge_cases.txt`
4. Ensure consistency across all languages

Example:
```python
# Python
'₹': 'INR',  # Indian Rupee symbol

# JavaScript
'₹': 'INR',  // Indian Rupee symbol

# PHP
'₹' => 'INR',  // Indian Rupee symbol

# Bash
-e 's/₹/INR/g'  # Indian Rupee symbol
```

### Testing Requirements

1. All changes must pass `validate_slug_scripts`
2. Add relevant test cases for new features
3. Update unit tests if applicable
4. Test with all parameter combinations

## 🏷️ Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

### Version Update Process

1. **Update version using the script:**
   ```bash
   ./update_version.sh 1.0.2
   ```

2. **Update CHANGELOG.md:**
   - Add new version section
   - Document all changes
   - Follow Keep a Changelog format

3. **Commit version bump:**
   ```bash
   git commit -am "chore: bump version to 1.0.2"
   ```

4. **Create and push tag:**
   ```bash
   git tag -a v1.0.2 -m "Version 1.0.2"
   git push origin v1.0.2
   ```

### Version File Locations

The `update_version.sh` script updates:
- `VERSION` - Single source of truth
- `post_slug.py` - `__version__` and docstring
- `post_slug.js` - `@version` comment
- `post_slug.php` - `@version` comment
- `post_slug.bash` - Version comment
- `slug-files` - Version comment
- `pyproject.toml` - Package version
- `README.md` - Footer version

## 🐛 Reporting Issues

1. Check existing issues first
2. Use issue templates when available
3. Include:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Language implementation affected
   - Test case if applicable

## 📝 Documentation

- Update relevant documentation for any changes
- Add docstring/comments for new functions
- Update README.md if adding features
- Keep examples current

## 🚀 Pull Request Process

1. **Title**: Use conventional commit format
2. **Description**: Explain what and why
3. **Testing**: Show test results
4. **Cross-language**: Confirm all implementations updated
5. **Documentation**: Note any doc updates

### PR Checklist

- [ ] All language implementations updated
- [ ] Tests pass (`validate_slug_scripts`)
- [ ] Documentation updated
- [ ] Version updated (if applicable)
- [ ] CHANGELOG.md updated
- [ ] No merge conflicts

## 💡 Development Tips

### Running Individual Tests

```bash
# Test specific implementation
./_post_slug.py "Test String"
./_post_slug.js "Test String"
./_post_slug.bash "Test String"
./_post_slug.php "Test String"

# Compare outputs
for impl in py js bash php; do
    echo -n "$impl: "
    ./_post_slug.$impl "Test String"
done
```

### Debugging Validation Failures

```bash
# Run validation in verbose mode
./validate_slug_scripts datasets/test.txt | less

# Test specific parameters
./validate_slug_scripts datasets/test.txt 0 '_' '1'
```

## 📦 Release Process

1. Ensure all tests pass
2. Update version (see Versioning section)
3. Update CHANGELOG.md
4. Create GitHub release
5. Build and publish packages:
   ```bash
   # Python
   python -m build
   python -m twine upload dist/*
   
   # npm (future)
   npm publish
   
   # Composer (future)
   # ...
   ```

## 🙏 Thank You!

Your contributions help make post_slug better for everyone. Whether it's fixing bugs, adding features, improving documentation, or reporting issues - every contribution matters!

If you have questions, feel free to open an issue or discussion.