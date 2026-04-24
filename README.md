# AI-Assisted Data Analysis Agent

**Riga Technical University — Systems Analysis & Design**  
*System Implementation, Testing, and Deployment*

---

## Overview

This project implements an **AI-assisted software system** in Python. A single intelligent agent (`ResearchAgent`) uses five specialized tools to:

- Perform mathematical calculations
- Analyze text and CSV data
- Convert between data formats (CSV, JSON, text)
- Generate structured reports with export capabilities

The system receives user input through a command-line interface, processes requests using appropriate tools, and returns meaningful results.

## Project Structure

```
├── src/                    # Source code
│   ├── main.py             # CLI entry point
│   ├── agent.py            # AI agent orchestrator
│   ├── tools/              # Specialized tool modules
│   │   ├── calculator.py
│   │   ├── text_analyzer.py
│   │   ├── csv_analyzer.py
│   │   ├── data_converter.py
│   │   └── report_generator.py
│   └── utils/              # Utility modules
│       ├── input_handler.py
│       └── output_handler.py
├── tests/                  # Test suite (65 tests)
│   ├── test_calculator.py
│   ├── test_text_analyzer.py
│   ├── test_csv_analyzer.py
│   ├── test_data_converter.py
│   ├── test_report_generator.py
│   ├── test_agent.py
│   └── test_integration.py
├── data/                   # Sample data files
│   ├── sample_data.csv
│   └── sample_data.json
├── docs/                   # Documentation
│   ├── developer_guide.md
│   └── user_guide.md
├── requirements.txt        # Dependencies
├── setup.py                # Package configuration
├── JOURNAL.md              # Development journal
└── README.md               # This file
```

## Quick Start

```bash
pip install -r requirements.txt
python -m src.main
```

## Commands

| Command | Description | Example |
|---|---|---|
| `calculate` | Perform a calculation | `calculate 5 + 3` |
| `analyze` | Analyze a data file | `analyze data/sample_data.csv` |
| `convert` | Convert file format | `convert data/sample_data.csv` |
| `report` | Generate a report | `report "My Analysis"` |
| `help` | Show available commands | `help` |
| `exit` | Exit the application | `exit` |

## Testing

```bash
python -m unittest discover -s tests -v
```

65 tests covering tools, agent logic, and end-to-end workflows.

## Documentation

- [User Guide](docs/user_guide.md) — how to install and use the system
- [Developer Guide](docs/developer_guide.md) — architecture, concepts, and extension guide
- [Development Journal](JOURNAL.md) — step-by-step project journal

## Deployment Strategy

The system is designed for **phased deployment**:
1. **Alpha** — local testing (current state)
2. **Beta** — controlled user testing with real data
3. **Production** — PyPI package or standalone executable
