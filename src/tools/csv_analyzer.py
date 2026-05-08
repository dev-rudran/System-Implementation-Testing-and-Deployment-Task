import csv
import os
from typing import Dict, List, Union


class CSVAnalyzerTool:
    def analyze(self, file_path: str) -> Dict[str, Union[str, int, float, list]]:
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        try:
            with open(file_path, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            if not rows:
                return {"error": "CSV file is empty."}

            field_names = list(rows[0].keys())
            row_count = len(rows)
            column_count = len(field_names)

            numeric_columns = {}
            text_columns = {}

            for col in field_names:
                numeric_values = []
                for row in rows:
                    val = row[col].strip()
                    try:
                        numeric_values.append(float(val))
                    except ValueError:
                        pass

                if numeric_values:
                    numeric_columns[col] = {
                        "min": min(numeric_values),
                        "max": max(numeric_values),
                        "avg": round(sum(numeric_values) / len(numeric_values), 2),
                        "sum": round(sum(numeric_values), 2),
                        "count": len(numeric_values),
                    }
                else:
                    text_values = [row[col].strip() for row in rows]
                    text_columns[col] = {
                        "unique_values": len(set(text_values)),
                        "sample_values": list(set(text_values))[:3],
                    }

            return {
                "file_path": file_path,
                "row_count": row_count,
                "column_count": column_count,
                "field_names": field_names,
                "numeric_columns": numeric_columns,
                "text_columns": text_columns,
            }

        except Exception as e:
            return {"error": f"Failed to analyze CSV: {e}"}

    def search(self, file_path: str, column: str, value: str) -> List[Dict[str, str]]:
        if not os.path.exists(file_path):
            return [{"error": f"File not found: {file_path}"}]

        try:
            with open(file_path, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                results = [row for row in reader if row.get(column, "").strip().lower() == value.lower()]
            return results if results else [{"message": f"No rows found where {column} = {value}"}]
        except Exception as e:
            return [{"error": f"Search failed: {e}"}]
