"""
Compatibility layer
"""
from collections import OrderedDict

__all__ = ('OrderedDict', 'first_key', 'first_value')


def first_key(obj):
    """Return the first key of a dict-like object."""
    return next(iter(obj))


def first_value(obj):
    """Return the first value of a dict-like object."""
    return next(iter(obj.values()))
