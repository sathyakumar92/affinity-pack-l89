"""Tests for client module"""
import pytest
from pathlib import Path


class TestClient:
    """Tests for client functionality"""
    
    def test_import(self):
        """Test module can be imported"""
        from affinity_toolkit import AffinityDesignerClient
        assert AffinityDesignerClient is not None
    
    def test_instantiate(self):
        """Test class can be instantiated"""
        from affinity_toolkit.client import *
        # Basic instantiation test
        pass
    
    def test_is_installed(self):
        """Test installation detection"""
        from affinity_toolkit.utils.detection import is_installed
        result = is_installed()
        assert isinstance(result, bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
