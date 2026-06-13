# catr

> A sleek terminal syntax highlighting file viewer — like `cat`, but prettier.

`catr` displays file contents in your terminal with full syntax highlighting, line numbers, file metadata, and a clean formatted layout powered by [Pygments](https://pygments.org/).

---

## Features

- **Syntax highlighting** for hundreds of languages (Python, C, JavaScript, YAML, and more)
- **Line numbers** with aligned gutter
- **File metadata** — filename, size in bytes, and total line count
- **Binary file detection** — gracefully handles non-text files
- **Colorized output** using true-color terminal support
- Works as a global CLI command after installation

---

## Installation

```bash
pip install catr
```

Or install from source:

```bash
git clone https://github.com/your-username/catr.git
cd catr
pip install .
```

---

## Dependencies
- [`Pygments`](https://pypi.org/project/Pygments/) for syntax highlighting
- [`colored`](https://pypi.org/project/colored/) for terminal color output

## Usage

```bash
catr <file_path>
```

### Examples

```bash
catr src/catr/catr.py
catr README.md
catr config.yaml
```

### Sample Output

```
────────────────────────────────────────────────────────────────────────────────────────────────────
    catr.py (2048 bytes) | 72 lines
────────────────────────────────────────────────────────────────────────────────────────────────────
 1 │ import sys
 2 │ from pygments import highlight
 3 │ ...
────────────────────────────────────────────────────────────────────────────────────────────────────
: < END OF FILE >
════════════════════════════════════════════════════════════════════════════════════════════════════
```

---

## Requirements

- Python >= 3.8
- [`pygments`](https://pypi.org/project/Pygments/) >= 2.17.0
- [`colored`](https://pypi.org/project/colored/) >= 1.4.4

---

## Project Structure

```
catr/
├── src/
│   └── catr/
│       ├── __init__.py
│       └── catr.py
├── pyproject.toml
└── README.md
```

---

## License

See [LICENSE](LICENSE) for details.

---

## Author

**Juan Jose Solorzano Carrillo** — juanjose.solorzano.c@gmail.com
