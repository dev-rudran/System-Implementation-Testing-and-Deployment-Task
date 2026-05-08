import csv
import json
import os
from typing import Dict, List, Union


class DataConverterTool:
    def csv_to_json(self, csv_path: str, json_path: str = None) -> Union[str, Dict]:
        if not os.path.exists(csv_path):
            return {"error": f"CSV file not found: {csv_path}"}

        try:
            with open(csv_path, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                data = list(reader)

            if not json_path:
                json_path = csv_path.rsplit(".", 1)[0] + ".json"

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return {
                "message": f"Successfully converted {csv_path} to {json_path}",
                "output_path": json_path,
                "records_converted": len(data),
            }
        except Exception as e:
            return {"error": f"CSV to JSON conversion failed: {e}"}

    def json_to_csv(self, json_path: str, csv_path: str = None) -> Union[str, Dict]:
        if not os.path.exists(json_path):
            return {"error": f"JSON file not found: {json_path}"}

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not data:
                return {"error": "JSON data is empty."}

            if isinstance(data, dict):
                data = [data]

            if not csv_path:
                csv_path = json_path.rsplit(".", 1)[0] + ".csv"

            fieldnames = list(data[0].keys())
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)

            return {
                "message": f"Successfully converted {json_path} to {csv_path}",
                "output_path": csv_path,
                "records_converted": len(data),
            }
        except Exception as e:
            return {"error": f"JSON to CSV conversion failed: {e}"}

    def convert_text_to_json(self, text_path: str, json_path: str = None) -> Union[str, Dict]:
        if not os.path.exists(text_path):
            return {"error": f"Text file not found: {text_path}"}

        try:
            with open(text_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            data = {"filename": os.path.basename(text_path), "line_count": len(lines), "content": "".join(lines)}

            if not json_path:
                json_path = text_path.rsplit(".", 1)[0] + ".json"

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return {
                "message": f"Successfully converted {text_path} to {json_path}",
                "output_path": json_path,
            }
        except Exception as e:
            return {"error": f"Text to JSON conversion failed: {e}"}
