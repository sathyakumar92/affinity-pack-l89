# Affinity Designer for Windows Toolkit Documentation

## Quick Start

```python
from affinity_toolkit import AffinityDesignerClient

client = AffinityDesignerClient()
if client.is_installed():
    client.connect()
    print(f"Version: {client.get_version()}")
```

## API Reference

See individual module documentation.
