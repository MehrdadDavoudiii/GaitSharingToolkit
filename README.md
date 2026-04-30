# Gait Sharing

A free, open-source toolkit for data management and decision-making in clinical gait analysis.

**Author**: Mehrdad Davoudi, University Children's Hospital Basel (UKBB), Basel, Switzerland

📖 **[Documentation](https://mehrdaddavoudiii.github.io/GaitSharingToolkit/)** · 📄 **[Tutorial (PDF)](https://github.com/MehrdadDavoudiii/GaitSharingToolkit/blob/main/Toturial/GaitSharing_Tutorial.pdf)**

---

## Overview

Gait Sharing provides a complete pipeline from raw clinical data to AI-assisted gait interpretation:

| Step | Module | Description |
|------|--------|-------------|
| 1 | **Import** | Import patient data from existing lab databases |
| 2 | **Patients** | View, edit, and manage patient records |
| 3 | **Search** | Filter patients by clinical criteria |
| 4 | **Export** | Create secondary databases for research |
| 5 | **Anonymizer** | Anonymize clinical reports for sharing |
| 6 | **C3D Extractor** | Extract gait data from C3D files to Excel |
| 7 | **Stride Analysis** | Segment gait cycles into individual strides |
| 8 | **Feature Extraction** | Compute biomechanical features per stride |
| 9 | **AI Interpreter** | Generate AI-assisted gait reports via ChatGPT |

## Installation

The toolkit has been developed with **Python 3.13**. Although Python 3.14 is available, the `ezc3d` library does not yet provide pre-built wheels for this version. Therefore, Python 3.13 is recommended to ensure full compatibility with all dependencies.

```bash
pip install -r requirements.txt
python GaitSharing_main.py
```

## Dependencies

| Package | Purpose |
|---------|---------|
| PySide6 | Graphical user interface (Qt) |
| numpy | Numerical computations |
| scipy | Signal processing and interpolation |
| openpyxl | Excel file I/O |
| PyMuPDF | PDF parsing and anonymization |
| ezc3d | C3D biomechanical file reading |
| openai | AI Interpreter (ChatGPT integration) |
| python-docx | DOCX report export |
| Pillow | Image processing |

## Key Features

- **Multilingual PDF parsing**: Extracts patient data from clinical reports in German, French, Italian, and English
- **Automated anonymization**: Removes personally identifiable information from PDF reports with standard or enhanced redaction
- **C3D to Excel conversion**: Makes biomechanical data accessible without specialized software
- **Stride-level feature extraction**: Computes min, max, mean, range, and timing features per gait cycle phase
- **Reference data comparison**: Compares patient gait features against healthy reference values
- **AI-assisted reporting**: Generates clinical gait descriptions using ChatGPT with customizable prompts
- **Privacy-aware design**: Patient names stay local and are never transmitted to external APIs

## Contact

- **Email**: Mehrdad.davoudi@ukbb.ch
- **Institution**: University Children's Hospital Basel (UKBB), Switzerland
- **GitHub**: https://github.com/MehrdadDavoudiii
- **LinkedIn**: https://www.linkedin.com/in/mehrdad-davoudi-profile/

## Citing

If you use Gait Sharing in your research, please cite:

```bibtex
@software{davoudi2025gaitsharing,
  author    = {Davoudi, Mehrdad},
  title     = {Gait Sharing: A Toolkit for Clinical Gait Analysis},
  year      = {2025},
  publisher = {GitHub},
  url       = {https://github.com/MehrdadDavoudiii/GaitSharing}
}
```
