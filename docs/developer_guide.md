# Developer Guide — AI-Assisted Data Analysis Agent

## Project Overview

This project implements an **AI-assisted software system** in Python that acts as a **single intelligent agent** capable of using multiple tools to solve data analysis tasks. The agent receives user input, processes it through a command-based interface, invokes appropriate tools, and returns meaningful results.

## System Architecture

```
src/
├── main.py              # Entry point — CLI loop
├── agent.py             # ResearchAgent — orchestrator
├── tools/
│   ├── calculator.py    # CalculatorTool
│   ├── text_analyzer.py # TextAnalyzerTool
│   ├── csv_analyzer.py  # CSVAnalyzerTool
│   ├── data_converter.py# DataConverterTool
│   └── report_generator.py # ReportGeneratorTool
└── utils/
    ├── input_handler.py # InputHandler — parses user commands
    └── output_handler.py# OutputHandler — formats results

tests/
├── test_calculator.py
├── test_text_analyzer.py
├── test_csv_analyzer.py
├── test_data_converter.py
├── test_report_generator.py
├── test_agent.py
└── test_integration.py

data/
├── sample_data.csv
└── sample_data.json

docs/
├── developer_guide.md
└── user_guide.md
```

## Programming Concepts Used

| Concept | Usage in Project |
|---|---|
| **Object-Oriented Programming** | Each tool is a class with a public interface; the agent uses composition to hold tool instances. |
| **Modular Design (Packages)** | Code is split into `tools/`, `utils/`, and tests are in a separate `tests/` package. |
| **Error Handling (try/except)** | Tools handle file I/O errors, division by zero, missing files, and unexpected input gracefully. |
| **Input Validation** | `InputHandler` validates commands and arguments before dispatching to the agent. |
| **Data Serialization (JSON/CSV)** | `DataConverterTool` handles cross-format conversion; `ReportGeneratorTool` exports reports in JSON and plain text. |
| **Unit Testing (unittest)** | 65 test cases across 7 test files covering tools, agent, and integration scenarios. |
| **Composition (has-a)** | `ResearchAgent` composes all five tools and both utility handlers. |
| **Strategy Pattern** | Command dispatch in `agent.py` uses a handler dictionary (`handlers` dict) to route commands to methods. |

## Tool Integration

Each tool is an independent module with a single public method. The agent composes all tools and delegates based on the parsed command:

1. **CalculatorTool** — performs safe arithmetic (addition, subtraction, multiplication, division, exponentiation, modulo, sqrt, rounding).
2. **TextAnalyzerTool** — analyzes text (word count, character count, sentence count, unique words, word frequency).
3. **CSVAnalyzerTool** — reads and analyzes CSV files (row/column counts, numeric stats, text column samples, search).
4. **DataConverterTool** — converts between CSV, JSON, and plain text formats.
5. **ReportGeneratorTool** — generates structured reports and exports to JSON or plain text.

## Data Flow

```
User Input → InputHandler.parse()
  → Agent.process()
    → handler method (calculate/analyze/convert/report)
      → tool method call
        → result returned to agent
          → OutputHandler.display_result()
            → User sees formatted output
```

## Testing

Run all tests:
```bash
python -m unittest discover -s tests -v
```

Run a single test file:
```bash
python -m unittest tests.test_calculator -v
```

## Extending the System

To add a new tool:
1. Create a new file in `src/tools/` with a class exposing a public method.
2. Add the tool to `src/tools/__init__.py`.
3. Add the tool instance to `ResearchAgent.__init__()` in `src/agent.py`.
4. Add a handler method (e.g., `_handle_newtool`) and register it in the `handlers` dict.
5. Add the command to `InputHandler.supported_commands`.
6. Write tests in `tests/test_newtool.py`.
