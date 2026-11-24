"""Check each detected ScanCode expression against the file's approved policy keys."""

import json
import sys

from license_expression import ExpressionError, Licensing


LICENSING = Licensing()


def is_approved(expression, approved_keys):
    try:
        parsed = LICENSING.parse(expression)
    except ExpressionError:
        return False

    if parsed is None:
        return False

    # A WITH expression is one symbol, so approving its base license isn't enough.
    values = {
        symbol: LICENSING.TRUE if str(symbol) in approved_keys else LICENSING.FALSE
        for symbol in parsed.symbols
    }
    return parsed.subs(values).simplify() == LICENSING.TRUE


def main(report_path):
    with open(report_path, encoding="utf-8") as report:
        files = json.load(report)["files"]

    failures = []
    for resource in files:
        if not resource.get("license_detections"):
            continue

        expression = resource.get("detected_license_expression")
        approved_keys = {
            entry["license_key"]
            for entry in (resource.get("license_policy") or [])
            if entry["policy"] == "approved"
        }
        if not is_approved(expression, approved_keys):
            failures.append(f"  {resource['path']}: {expression or '<missing license expression>'}")

    if failures:
        print("Unapproved license expressions:", *failures, sep="\n")
        return 1

    print("All detected license expressions satisfy the policy.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
