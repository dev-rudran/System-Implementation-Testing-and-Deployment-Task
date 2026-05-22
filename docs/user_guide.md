# User Guide — AI-Assisted Data Analysis Agent

## What is This?

This is an **AI-assisted command-line tool** that helps you analyze data, perform calculations, convert file formats, and generate reports. You interact with it by typing commands.

## Installation

1. Ensure Python 3.10 or later is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python -m src.main
```

Or install as a package:
```bash
pip install -e .
ai-research-agent
```

## Available Commands

### `help`
Shows all available commands with examples.

### `calculate <expression>`
Performs a mathematical calculation.
```
> calculate 5 + 3
> calculate 10 / 4
> calculate sqrt(16)
> calculate round(3.14159, 2)
```

### `analyze <file_path>`
Analyzes a CSV, JSON, or text file.

For CSV files:
```
> analyze data/sample_data.csv
```
Shows row/column count, field names, numeric statistics (min/max/avg/sum), and text column info.

For text files:
```
> analyze data/sample.txt
```
Shows word count, character count, sentence count, unique words, and top word frequencies.

### `convert <file_path>`
Converts between file formats.
- `.csv` → converts to `.json`
- `.json` → converts to `.csv`
- `.txt` → converts to `.json`
```
> convert data/sample_data.csv
```

### `report <title>`
Generates a structured report from all previous analysis results.
```
> report "My Analysis Results"
```
The report is displayed and saved to a `.json` file.

### `exit`
Closes the application.

## Example Workflow

```
> calculate 45 * 3
> analyze data/sample_data.csv
> convert data/sample_data.csv
> report "Complete Analysis"
> exit
```

## Sample Data

Sample files are provided in the `data/` directory:
- `sample_data.csv` — student records (name, age, grade, city, score)
- `sample_data.json` — course information (id, name, credits, instructor)

You can use these to test the system or replace them with your own data.

## Configuration

No environment variables are required. The system runs entirely locally. All configuration is handled through command-line interaction.
