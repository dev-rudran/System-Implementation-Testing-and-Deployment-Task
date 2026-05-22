# Project Journal — AI-Assisted Data Analysis Agent

**University:** Riga Technical University  
**Course:** Systems Analysis & Design  
**Topic:** System Implementation, Testing, and Deployment  
**Student Project**

---

## Step 1 (24.04) — Planning

### System Description and Goal

The planned system is an **AI-assisted data analysis agent** — a Python program that acts as an intelligent assistant capable of:
- Receiving user queries through a command-line interface,
- Dispatching requests to appropriate internal tools,
- Performing data analysis, format conversion, calculations, and report generation,
- Returning structured results to the user.

The goal is to build a modular, testable, and deployable Python system that demonstrates the complete software development lifecycle from design through implementation, testing, and deployment preparation.

### AI / Agent-Based Approach

The system follows a **single intelligent agent architecture**. The `ResearchAgent` class acts as the central orchestrator. It:
- Receives parsed input from the `InputHandler`,
- Decides which tool to invoke based on the command,
- Collects results and passes them to the `OutputHandler` for display,
- Maintains session state so later commands (e.g., `report`) can use earlier results.

This reflects the **agent-based paradigm** where an autonomous entity perceives input, acts upon it using tools, and returns a response.

### Planned Tools

| Tool | Purpose |
|---|---|
| `CalculatorTool` | Perform safe arithmetic and mathematical operations |
| `TextAnalyzerTool` | Analyze text content (word count, frequency, readability) |
| `CSVAnalyzerTool` | Read and analyze CSV data files |
| `DataConverterTool` | Convert between CSV, JSON, and plain text formats |
| `ReportGeneratorTool` | Compile results into structured reports and export them |

### Programming Concepts Required

- Object-Oriented Programming (classes, composition)
- Modular design (packages and modules)
- File I/O (reading/writing CSV, JSON, text files)
- Exception handling
- Unit testing (unittest framework)
- Data serialization (JSON, CSV)
- Git version control

---

## Step 2 (08.05) — Implementation Progress

### Updated System Description

The system has been implemented as planned with all five tools fully functional. The architecture remained stable throughout implementation. Key design decisions:
- Each tool is an independent class in its own module under `src/tools/`,
- The agent uses composition to hold all tool instances,
- A command dispatcher pattern routes parsed commands to handler methods,
- Session state is stored in `self.session_results` dict for cross-command data sharing.

### Programming Concepts Actually Used

| Concept | How It Is Applied |
|---|---|
| **Classes and Objects** | Each tool, the agent, and both handlers are defined as classes with constructors (`__init__`) and public methods. |
| **Composition** | `ResearchAgent` has-a `CalculatorTool`, `TextAnalyzerTool`, etc. |
| **Polymorphism** | All tools follow the same pattern — instantiated once, method called with arguments, result returned. |
| **Error Handling** | Every tool wraps risky operations in try/except blocks; the agent checks for error keys in results. |
| **Data Serialization** | JSON reading/writing via `json` module; CSV reading/writing via `csv.DictReader`/`DictWriter`. |
| **Command Pattern** | The `handlers` dictionary maps command names to methods, enabling clean dispatch. |
| **String Manipulation** | `TextAnalyzerTool` uses regex (`re.split`) for sentence detection and string methods for word frequency. |
| **File I/O** | All tools that handle files use context managers (`with open(...)`) for safe resource handling. |

### Tool Integration

Tools are integrated into the agent as follows:

1. **Initialization** — All five tools are instantiated in `ResearchAgent.__init__()`.
2. **Dispatch** — `InputHandler.parse_input()` extracts the command and argument; `process()` looks up the handler method in a dictionary.
3. **Handler Methods** — Each handler (e.g., `_handle_calculate`) calls the corresponding tool method, stores the result in `self.session_results`, and returns a structured dict.
4. **Output** — `OutputHandler.display_result()` formats the dict for console display (JSON for data, formatted text for reports, errors in red).

---

## Step 3 (15.05) — Testing and Deployment Preparation

### Testing Process

Testing was performed **together with implementation** using Python's built-in `unittest` framework. Seven test files were created, covering 65 test scenarios in total:

| Test File | Test Count | Scope |
|---|---|---|
| `test_calculator.py` | 13 | Addition, subtraction, multiplication, division, edge cases (zero division, negatives, sqrt, round) |
| `test_text_analyzer.py` | 11 | Word count, character count, sentences, unique words, empty text, punctuation handling |
| `test_csv_analyzer.py` | 8 | Row/column count, numeric stats, file-not-found, search, empty CSV |
| `test_data_converter.py` | 6 | CSV→JSON, JSON→CSV, text→JSON, file-not-found, error handling |
| `test_report_generator.py` | 5 | Report structure, error handling, JSON export, text export, empty results |
| `test_agent.py` | 14 | Command parsing, error handling, session tracking, all commands |
| `test_integration.py` | 8 | End-to-end workflows, roundtrip conversion, multi-format export |

### Test Scenarios and Explanations

1. **Functional Testing** — Full workflows (calculate → report, analyze → report) verify the system produces correct outputs.
2. **Tool Testing** — Each tool is tested independently with known inputs and expected outputs.
3. **Input Validation Testing** — Empty input, missing arguments, unknown commands, and non-existent files are tested.
4. **Error Handling Testing** — Division by zero, file-not-found, unsupported formats, and empty data are tested.
5. **Data Conversion Roundtrip** — CSV → JSON → CSV verifies no data loss during format conversion.

### Deployment Preparation

The system is prepared for deployment as follows:

1. **Dependencies** — Listed in `requirements.txt` (minimal — only `requests` is listed for future extensibility; currently no external dependencies are required).
2. **Installation** — Users can install via `pip install -r requirements.txt` or `pip install -e .`.
3. **Startup** — Run with `python -m src.main` or the `ai-research-agent` console script.
4. **Configuration** — No environment variables or configuration files are needed. The system runs out of the box.
5. **File Structure** — Clear separation of source code (`src/`), tests (`tests/`), data (`data/`), and documentation (`docs/`).

### Data Conversion / Porting

Data flows between components as follows:

1. **Input Format** — User provides commands and file paths as text. Files can be `.csv` (tabular data), `.json` (structured records), or `.txt` (plain text).
2. **Conversion** — `DataConverterTool` reads source files, deserializes them, and writes to the target format. CSV uses `csv.DictReader/DictWriter`, JSON uses `json.load/dump`.
3. **Analysis** — `CSVAnalyzerTool` reads CSV data and extracts numeric/text statistics. `TextAnalyzerTool` processes text content through string operations.
4. **Report** — `ReportGeneratorTool` aggregates results from multiple tools into a structured report dict and exports to JSON or plain text.
5. **Consistency** — Data correctness is preserved through:
   - UTF-8 encoding for all file operations,
   - `utf-8-sig` for CSV reading (handles BOM),
   - Type checking (numeric vs text column detection in CSV analysis),
   - Error propagation (tools return error dicts, agent checks for them).

---

## Final Submission (22.05) — Final Version

### Final System Description

The **AI-Assisted Data Analysis Agent** is a fully functional Python system that:
- Accepts user commands via an interactive CLI,
- Uses five specialized tools to process data,
- Maintains session state across commands,
- Generates structured reports with export capability,
- Handles errors gracefully with informative messages.

The system is complete with 65 passing tests, comprehensive documentation, and deployment-ready configuration.

### Final Programming Concepts and Usage

All previously listed concepts were successfully applied. Key refinements during development:
- **Graceful degradation** — If any tool fails (file not found, bad format, division by zero), the error is caught, wrapped in a dict with an "error" key, and displayed to the user without crashing.
- **Session management** — Results from `calculate` and `analyze` are stored in `session_results` so `report` can compile them even if they were run at different times.

### Final Tools and Their Roles

| Tool | Role in System |
|---|---|
| `CalculatorTool` | Provides mathematical computation capability — supports basic arithmetic, sqrt, and rounding. |
| `TextAnalyzerTool` | Analyzes textual data — essential for processing non-tabular input (readme files, notes, logs). |
| `CSVAnalyzerTool` | Core data analysis tool — reads structured tabular data and extracts meaningful statistics. |
| `DataConverterTool` | Enables interoperability between data formats — CSV, JSON, and text. |
| `ReportGeneratorTool` | Synthesizes results from all other tools into a coherent, exportable report. |

### Final Testing Results

**65 tests — all passing.**

- All tool tests confirm correct behavior with valid and invalid inputs.
- Agent tests confirm correct command routing, error handling, and session management.
- Integration tests confirm end-to-end workflows work correctly.

### Deployment Preparation (Final)

The system is deployment-ready:
- **Local CLI tool** — run with `python -m src.main`,
- **Package** — installable via `pip install -e .`,
- **Dependencies** — minimal (`requirements.txt`),
- **No external services** — works entirely offline,
- **Documentation provided** — both developer and user guides.

### Deployment Strategy

The recommended deployment strategy for this system is **phased deployment**:

1. **Alpha (local testing)** — The current state; the system runs locally on the developer's machine with sample data.
2. **Beta (controlled user testing)** — Distribute to a small group of users (e.g., classmates) who test with their own data. Collect feedback on command usability and edge cases.
3. **Production (general release)** — After beta fixes, the system can be distributed as a Python package on PyPI or as a standalone executable (via PyInstaller) for users without Python installed.

This staged approach ensures:
- Defects are caught before wide release,
- Users can provide feedback on the command interface,
- The system can be validated with real-world data before final release.

### GitHub Repository

The complete project with full commit history is available on GitHub. The repository shows the evolution from initial project setup through implementation, testing, documentation, and deployment preparation.
