"""
Affinity Designer for Windows Toolkit - Python automation and utilities

A comprehensive toolkit for working with Affinity Designer for Windows files and automation.
"""
from .client import AffinityDesignerClient
from .processor import AffinityDesignerProcessor
from .metadata import AffinityDesignerMetadataReader
from .batch import BatchProcessor
from .exporter import DataExporter

__version__ = "0.1.0"
__author__ = "Open Source Community"

__all__ = [
    "AffinityDesignerClient",
    "AffinityDesignerProcessor",
    "AffinityDesignerMetadataReader",
    "BatchProcessor",
    "DataExporter",
]
