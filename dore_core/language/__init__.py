"""Doré universal language and textual intelligence core."""
from .base import TextWitness, LanguageUnit, AdapterCapabilities, LanguageAdapter, validate_units
from .registry import LanguageRegistry

__all__ = [
    "TextWitness", "LanguageUnit", "AdapterCapabilities", "LanguageAdapter",
    "validate_units", "LanguageRegistry",
]
