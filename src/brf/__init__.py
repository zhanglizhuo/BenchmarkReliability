from .analyzer import BRFAnalyzer

__all__ = ["BRFAnalyzer"]

# Registry is lazily imported to avoid circular dependencies
# Use: from brf.registry import REGISTRY_SOURCES, list_sources
