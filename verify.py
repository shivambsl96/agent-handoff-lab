import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = "data/inventory.csv"
METRIC = "active_records"


def validate_report(report):
    return (
        isinstance(report, dict)
        and report.get("status") == "done"
        and report.get("source") == SOURCE
        and report.get("metric") == METRIC
        and type(report.get("value")) is int
        and report["value"] >= 0
    )


def main():
    parser = argparse.ArgumentParser(description="Check a worker's inventory count.")
    parser.add_argument("report", type=Path)
    parser.add_argument("--format-only", action="store_true")
    args = parser.parse_args()

    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
        if not validate_report(report):
            print("REJECTED: invalid handoff format, source or metric")
            return 1

        print(f"FORMAT ACCEPTED: {METRIC} = {report['value']}")
        if args.format_only:
            return 0

        with (ROOT / SOURCE).open(encoding="utf-8", newline="") as inventory:
            active = sum(row["status"] == "active" for row in csv.DictReader(inventory))

        if report["value"] != active:
            print(f"SOURCE REJECTED: reported {report['value']}, counted {active} active records")
            return 1

        print(f"SOURCE VERIFIED: counted {active} active records")
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(f"REJECTED: could not read report or inventory ({error})")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
