#!/bin/bash
# Update version across all files in the post_slug project

set -euo pipefail

# Check if version argument provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <new_version>"
    echo "Example: $0 1.0.2"
    exit 1
fi

NEW_VERSION="$1"

# Validate version format (basic check)
if ! [[ "$NEW_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Version must be in format X.Y.Z (e.g., 1.0.2)"
    exit 1
fi

echo "Updating version to $NEW_VERSION..."

# Update VERSION file
echo "$NEW_VERSION" > VERSION
echo "✓ Updated VERSION file"

# Update Python __version__
sed -i "s/__version__ = '[^']*'/__version__ = '$NEW_VERSION'/" post_slug.py
echo "✓ Updated post_slug.py"

# Update Python docstring version
sed -i "/^  Version:/,/^  --------/ s/^  [0-9]\+\.[0-9]\+\.[0-9]\+$/  $NEW_VERSION/" post_slug.py
echo "✓ Updated post_slug.py docstring"

# Update JavaScript @version
sed -i "s/@version [0-9]\+\.[0-9]\+\.[0-9]\+/@version $NEW_VERSION/" post_slug.js
echo "✓ Updated post_slug.js"

# Update PHP @version
sed -i "s/@version [0-9]\+\.[0-9]\+\.[0-9]\+/@version $NEW_VERSION/" post_slug.php
echo "✓ Updated post_slug.php"

# Update Bash version
sed -i "s/# Version: [0-9]\+\.[0-9]\+\.[0-9]\+/# Version: $NEW_VERSION/" post_slug.bash
echo "✓ Updated post_slug.bash"

# Update slug-files version
sed -i "s/# Version: [0-9]\+\.[0-9]\+\.[0-9]\+/# Version: $NEW_VERSION/" slug-files
echo "✓ Updated slug-files"

# Update pyproject.toml
sed -i "s/^version = \"[^\"]*\"/version = \"$NEW_VERSION\"/" pyproject.toml
echo "✓ Updated pyproject.toml"

# Update README.md footer
sed -i "s/\*\*Version\*\*: [0-9]\+\.[0-9]\+\.[0-9]\+/**Version**: $NEW_VERSION/" README.md
echo "✓ Updated README.md"

echo ""
echo "Version updated to $NEW_VERSION in all files!"
echo ""
echo "Don't forget to:"
echo "1. Update CHANGELOG.md with the new version details"
echo "2. Commit the changes: git commit -am \"chore: bump version to $NEW_VERSION\""
echo "3. Create a git tag: git tag -a v$NEW_VERSION -m \"Version $NEW_VERSION\""
echo "4. Push the tag: git push origin v$NEW_VERSION"