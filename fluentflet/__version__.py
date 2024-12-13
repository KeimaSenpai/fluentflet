__version__ = "0.1.0"

# Optional: Add version components
VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_PATCH = 0
VERSION_INFO = (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)

VERSION_STATUS = "alpha"  # "alpha", "beta", "rc", "final"
VERSION_BUILD = 1

# Full version string
VERSION = f"{__version__}"
if VERSION_STATUS != "final":
    VERSION += f"{VERSION_STATUS}{VERSION_BUILD}"