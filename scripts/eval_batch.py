import argparse
import json
import sys
from pathlib import Path

# Allow running the script from repo root without installing as a package
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from backend.app.services.evaluation import compute_metrics, load_mcq_file


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch evaluation (acceptance, fairness, latency).")
    parser.add_argument("input", type=Path, help="Path to MCQ file (JSONL or JSON list).")
    parser.add_argument("--group-field", default="language", help="Field to use for fairness grouping (default: language).")
    parser.add_argument("--output", type=Path, default=None, help="Optional path to write metrics JSON.")
    args = parser.parse_args()

    items = load_mcq_file(args.input)
    metrics = compute_metrics(items, group_field=args.group_field)
    print(json.dumps(metrics, indent=2, ensure_ascii=False))

    if args.output:
        args.output.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
