"""Summarize veraPDF's JSON reports (PDF/UA-1): one line per failed rule, with how many times it failed.
Exits 1 if any PDF isn't compliant. Used by the website workflow (M13)."""
import json
import sys


def jobs(report):
    return report.get("report", report).get("jobs", [])


def main(paths):
    bad = False
    for path in paths:
        try:
            report = json.load(open(path))
        except (OSError, ValueError) as e:
            print(f"{path}: no report ({e})")
            bad = True
            continue
        for job in jobs(report):
            name = job.get("itemDetails", {}).get("name", path)
            for vr in job.get("validationResult", []) if isinstance(job.get("validationResult"), list) else [job.get("validationResult", {})]:
                ok = vr.get("compliant")
                details = vr.get("details", {})
                print(f"{name}: {'PASS' if ok else 'FAIL'} ({details.get('failedRules', 0)} rules failed, {details.get('failedChecks', 0)} checks)")
                for rule in details.get("ruleSummaries", []):
                    if rule.get("ruleStatus") == "FAILED" or rule.get("status") == "failed":
                        print(f"  {rule.get('specification', '')} {rule.get('clause')}-{rule.get('testNumber')}: "
                              f"{rule.get('failedChecks')} times. {rule.get('description', '').strip()}")
                        for check in rule.get("checks", [])[:2]:
                            print(f"      e.g. {check.get('context', '')[:160]}")
                bad = bad or not ok
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
