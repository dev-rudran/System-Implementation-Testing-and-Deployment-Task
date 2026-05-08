import json
from datetime import datetime
from typing import Any, Dict, List, Union


class ReportGeneratorTool:
    def __init__(self):
        self.template = {
            "report_title": "",
            "generated_at": "",
            "summary": "",
            "findings": [],
            "statistics": {},
            "conclusion": "",
        }

    def generate_report(
        self, title: str, analysis_results: Dict[str, Any], conclusion: str = ""
    ) -> Dict[str, Any]:
        report = dict(self.template)
        report["report_title"] = title
        report["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        summary_parts = []
        findings = []

        for component, result in analysis_results.items():
            if isinstance(result, dict):
                if "error" in result:
                    findings.append(
                        {"component": component, "status": "error", "detail": result["error"]}
                    )
                    summary_parts.append(f"{component}: failed")
                else:
                    findings.append(
                        {"component": component, "status": "success", "detail": result}
                    )
                    summary_parts.append(f"{component}: completed")
            else:
                findings.append(
                    {"component": component, "status": "success", "detail": {"value": result}}
                )
                summary_parts.append(f"{component}: completed")

        report["summary"] = "; ".join(summary_parts)
        report["findings"] = findings
        report["statistics"] = self._extract_statistics(analysis_results)
        report["conclusion"] = conclusion or "Analysis completed successfully."

        return report

    def _extract_statistics(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        stats = {}
        for component, result in analysis_results.items():
            if isinstance(result, dict):
                stats[component] = {
                    k: v
                    for k, v in result.items()
                    if isinstance(v, (int, float, str))
                }
        return stats

    def export_to_json(self, report: Dict[str, Any], output_path: str) -> Union[str, Dict]:
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            return {
                "message": f"Report exported to {output_path}",
                "output_path": output_path,
            }
        except Exception as e:
            return {"error": f"Failed to export report: {e}"}

    def export_to_text(self, report: Dict[str, Any], output_path: str) -> Union[str, Dict]:
        try:
            lines = []
            lines.append("=" * 60)
            lines.append(f"REPORT: {report.get('report_title', 'Untitled')}")
            lines.append(f"Generated: {report.get('generated_at', 'Unknown')}")
            lines.append("=" * 60)
            lines.append("")
            lines.append("SUMMARY")
            lines.append("-" * 40)
            lines.append(report.get("summary", "No summary available."))
            lines.append("")
            lines.append("FINDINGS")
            lines.append("-" * 40)
            for finding in report.get("findings", []):
                status_icon = "[OK]" if finding.get("status") == "success" else "[FAIL]"
                lines.append(f"  {status_icon} {finding.get('component', 'Unknown')}")
                detail = finding.get("detail", {})
                if isinstance(detail, dict):
                    for k, v in detail.items():
                        if not isinstance(v, (dict, list)):
                            lines.append(f"      {k}: {v}")
            lines.append("")
            lines.append("STATISTICS")
            lines.append("-" * 40)
            for component, stats in report.get("statistics", {}).items():
                if stats:
                    lines.append(f"  {component}:")
                    for k, v in stats.items():
                        lines.append(f"    {k}: {v}")
            lines.append("")
            lines.append("CONCLUSION")
            lines.append("-" * 40)
            lines.append(report.get("conclusion", ""))
            lines.append("")
            lines.append("=" * 60)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))

            return {
                "message": f"Report exported to {output_path}",
                "output_path": output_path,
            }
        except Exception as e:
            return {"error": f"Failed to export text report: {e}"}
