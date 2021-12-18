# read version from installed package
try:
    from importlib.metadata import version
except Exception:
    from importlib_metadata import version
__version__ = version("imfpy")
##

