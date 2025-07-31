"""Version information for post_slug package."""

def get_version():
    """Read version from VERSION file."""
    import os
    version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
    with open(version_file, 'r') as f:
        return f.read().strip()

__version__ = get_version()