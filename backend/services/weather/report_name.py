import re


def to_file_name(report_name: str) -> str:
    sanitized = report_name.strip()
    has_wea_suffix = sanitized.lower().endswith(".wea")
    base = sanitized[:-4] if has_wea_suffix else sanitized
    base = re.sub(r"[^\w\s-]", "", base)
    base = re.sub(r"[\s-]+", "_", base)
    base = base.strip("_")
    if not base:
        base = "report"
    return f"{base}.wea"
