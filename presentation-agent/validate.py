"""Data Validation Agent — checks CSV quality before document generation.

Usage:
    python3.11 validate.py --app-csv portfolio.csv --infra-csv servers.csv

Outputs a quality score and list of issues to fix.
"""

import argparse
import csv
import os
import sys
from collections import Counter


def read_csv(path: str) -> list[dict]:
    """Read CSV file, handling BOM and flexible delimiters."""
    with open(path, "r", encoding="utf-8-sig") as f:
        content = f.read()
    content = content.lstrip("\ufeff")
    delimiter = "," if content.count(",") > content.count("\t") else "\t"
    reader = csv.DictReader(content.splitlines(), delimiter=delimiter, quotechar='"', skipinitialspace=True)
    rows = []
    for row in reader:
        cleaned = {k.strip().strip('"'): v.strip().strip('"') if v else "" for k, v in row.items() if k}
        rows.append(cleaned)
    return rows


def find_col(row: dict, candidates: list[str]) -> str | None:
    """Find a column by fuzzy matching against candidates."""
    for c in candidates:
        for key in row.keys():
            if c.lower() in key.lower():
                return key
    return None


EOL_PATTERNS = [
    "java 6", "java 7", "java 8", "python 2", "cobol", "vb6", "visual basic",
    ".net 4.0", ".net 4.5", ".net 4.6", ".net 4.8", "asp.net 4",
    "weblogic 10", "weblogic 11", "websphere 7", "websphere 8",
    "jboss 4", "jboss 5", "jboss 6", "struts 1",
    "windows server 2003", "windows server 2008", "windows server 2012",
    "rhel 5", "rhel 6", "centos 5", "centos 6",
    "oracle 10g", "oracle 11g", "sql server 2008", "sql server 2012",
    "mysql 5.5", "mysql 5.6", "postgresql 9",
    "node.js 10", "node.js 12", "node.js 14",
]


def validate_apps(rows: list[dict]) -> list[dict]:
    """Validate application portfolio CSV. Returns list of issues."""
    if not rows:
        return [{"severity": "CRITICAL", "field": "—", "issue": "Application CSV is empty", "affected": "All"}]

    issues = []
    sample = rows[0]

    name_col = find_col(sample, ["App_Name", "Application Name", "Name", "app_name"])
    crit_col = find_col(sample, ["Criticality", "SLA_Tier", "Priority"])
    lang_col = find_col(sample, ["Primary_Language", "Technology Stack", "Language", "Tech"])
    env_col = find_col(sample, ["Environment", "Env"])
    dep_col = find_col(sample, ["Integration_Dependencies", "Dependencies", "Integrated_Apps"])
    strategy_col = find_col(sample, ["Recommended Strategy", "Strategy", "R_Type"])
    id_col = find_col(sample, ["App_ID", "ID", "App ID"])

    # Check required columns exist
    if not name_col:
        issues.append({"severity": "CRITICAL", "field": "App Name", "issue": "No application name column found", "affected": "All"})
        return issues

    # Check for duplicates
    names = [row.get(name_col, "") for row in rows]
    dupes = [n for n, count in Counter(names).items() if count > 1 and n]
    if dupes:
        issues.append({"severity": "HIGH", "field": name_col, "issue": f"Duplicate application names: {', '.join(dupes)}", "affected": f"{len(dupes)} apps"})

    if id_col:
        ids = [row.get(id_col, "") for row in rows]
        id_dupes = [i for i, count in Counter(ids).items() if count > 1 and i]
        if id_dupes:
            issues.append({"severity": "HIGH", "field": id_col, "issue": f"Duplicate IDs: {', '.join(id_dupes)}", "affected": f"{len(id_dupes)} apps"})

    # Check each row
    missing_crit = []
    missing_tech = []
    missing_env = []
    missing_deps = []
    no_version = []
    eol_detected = []

    for row in rows:
        app_name = row.get(name_col, "Unknown")

        # Criticality missing
        if crit_col and not row.get(crit_col, "").strip():
            missing_crit.append(app_name)

        # Tech stack missing
        if lang_col:
            tech = row.get(lang_col, "").strip()
            if not tech:
                missing_tech.append(app_name)
            elif tech and not any(c.isdigit() for c in tech):
                no_version.append(app_name)
            # EOL detection
            tech_lower = tech.lower()
            for pattern in EOL_PATTERNS:
                if pattern in tech_lower:
                    eol_detected.append((app_name, pattern))
                    break

        # Environment missing
        if env_col and not row.get(env_col, "").strip():
            missing_env.append(app_name)

        # Dependencies missing for production apps
        if dep_col and env_col:
            env = row.get(env_col, "").strip().upper()
            deps = row.get(dep_col, "").strip()
            if env == "PRODUCTION" and not deps:
                missing_deps.append(app_name)

    # Compile issues
    if missing_crit:
        issues.append({"severity": "HIGH", "field": "Criticality", "issue": "Missing criticality rating", "affected": f"{len(missing_crit)} apps: {', '.join(missing_crit[:5])}"})

    if missing_tech:
        issues.append({"severity": "HIGH", "field": "Technology Stack", "issue": "Missing technology stack", "affected": f"{len(missing_tech)} apps: {', '.join(missing_tech[:5])}"})

    if no_version:
        issues.append({"severity": "MEDIUM", "field": "Technology Stack", "issue": "Tech stack missing version numbers (e.g., 'Java' instead of 'Java 17')", "affected": f"{len(no_version)} apps: {', '.join(no_version[:5])}"})

    if missing_env:
        issues.append({"severity": "MEDIUM", "field": "Environment", "issue": "Missing environment designation", "affected": f"{len(missing_env)} apps: {', '.join(missing_env[:5])}"})

    if missing_deps:
        issues.append({"severity": "MEDIUM", "field": "Dependencies", "issue": "Production apps with no dependencies listed (verify if truly standalone)", "affected": f"{len(missing_deps)} apps: {', '.join(missing_deps[:5])}"})

    if not crit_col:
        issues.append({"severity": "HIGH", "field": "Criticality", "issue": "No criticality/priority column found in CSV", "affected": "All"})

    if not lang_col:
        issues.append({"severity": "HIGH", "field": "Technology Stack", "issue": "No technology stack column found in CSV", "affected": "All"})

    if not strategy_col:
        issues.append({"severity": "LOW", "field": "Migration Strategy", "issue": "No 6Rs strategy column — agent will classify automatically but results may vary", "affected": "All"})

    # EOL info (not an issue, but useful signal)
    if eol_detected:
        issues.append({"severity": "INFO", "field": "EOL Detection", "issue": f"End-of-life technologies detected: {', '.join(set(p for _, p in eol_detected))}", "affected": f"{len(eol_detected)} apps"})

    return issues


def validate_infra(rows: list[dict]) -> list[dict]:
    """Validate infrastructure CSV. Returns list of issues."""
    if not rows:
        return [{"severity": "MEDIUM", "field": "—", "issue": "Infrastructure CSV is empty or not provided", "affected": "All"}]

    issues = []
    sample = rows[0]

    name_col = find_col(sample, ["Server Name", "server_name", "Hostname"])
    cpu_col = find_col(sample, ["CPU", "cpu_cores", "vCPU"])
    mem_col = find_col(sample, ["Memory", "RAM", "mem"])
    os_col = find_col(sample, ["Operating System", "OS", "os_name"])
    env_col = find_col(sample, ["Environment", "Env"])

    if not name_col:
        issues.append({"severity": "HIGH", "field": "Server Name", "issue": "No server name column found", "affected": "All"})
        return issues

    # Duplicates
    names = [row.get(name_col, "") for row in rows]
    dupes = [n for n, count in Counter(names).items() if count > 1 and n]
    if dupes:
        issues.append({"severity": "HIGH", "field": name_col, "issue": f"Duplicate server names: {', '.join(dupes)}", "affected": f"{len(dupes)} servers"})

    # Missing fields
    missing_cpu = []
    missing_mem = []
    missing_os = []

    for row in rows:
        srv = row.get(name_col, "Unknown")
        if cpu_col and not row.get(cpu_col, "").strip():
            missing_cpu.append(srv)
        if mem_col and not row.get(mem_col, "").strip():
            missing_mem.append(srv)
        if os_col and not row.get(os_col, "").strip():
            missing_os.append(srv)

    if missing_cpu:
        issues.append({"severity": "MEDIUM", "field": "CPU", "issue": "Missing CPU cores", "affected": f"{len(missing_cpu)} servers"})
    if missing_mem:
        issues.append({"severity": "MEDIUM", "field": "Memory", "issue": "Missing memory specification", "affected": f"{len(missing_mem)} servers"})
    if missing_os:
        issues.append({"severity": "MEDIUM", "field": "OS", "issue": "Missing operating system", "affected": f"{len(missing_os)} servers"})

    if not cpu_col:
        issues.append({"severity": "MEDIUM", "field": "CPU", "issue": "No CPU column found — right-sizing recommendations will be limited", "affected": "All"})
    if not os_col:
        issues.append({"severity": "MEDIUM", "field": "OS", "issue": "No OS column found — EOL OS detection unavailable", "affected": "All"})

    return issues


def calculate_score(app_issues: list[dict], infra_issues: list[dict]) -> int:
    """Calculate quality score 0-100."""
    score = 100
    for issue in app_issues + infra_issues:
        if issue["severity"] == "CRITICAL":
            score -= 30
        elif issue["severity"] == "HIGH":
            score -= 15
        elif issue["severity"] == "MEDIUM":
            score -= 5
        elif issue["severity"] == "LOW":
            score -= 2
    return max(0, score)


def print_report(app_rows: list[dict], infra_rows: list[dict], app_issues: list[dict], infra_issues: list[dict]):
    """Print the validation report."""
    score = calculate_score(app_issues, infra_issues)
    all_issues = app_issues + infra_issues

    print("=" * 60)
    print("  DATA QUALITY VALIDATION REPORT")
    print("=" * 60)
    print(f"\n  Applications: {len(app_rows)}")
    print(f"  Infrastructure: {len(infra_rows)}")
    print(f"  Issues found: {len([i for i in all_issues if i['severity'] != 'INFO'])}")
    print(f"\n  QUALITY SCORE: {score}/100", end="")
    if score >= 80:
        print("  ✅ READY — proceed with document generation")
    elif score >= 50:
        print("  ⚠️  ACCEPTABLE — review issues before generating")
    else:
        print("  ❌ NOT READY — fix critical/high issues first")

    print("\n" + "-" * 60)

    if not all_issues:
        print("\n  No issues found. Data is clean.")
        return

    # Group by severity
    for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]:
        sev_issues = [i for i in all_issues if i["severity"] == severity]
        if sev_issues:
            icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🔵", "INFO": "ℹ️"}[severity]
            print(f"\n  {icon} {severity}")
            for issue in sev_issues:
                print(f"     [{issue['field']}] {issue['issue']}")
                print(f"       Affected: {issue['affected']}")

    print("\n" + "-" * 60)
    print("\n  RECOMMENDATIONS:")
    if score < 50:
        print("  1. Fix all CRITICAL and HIGH issues before proceeding")
        print("  2. Re-run validation after fixes")
    elif score < 80:
        print("  1. Fix HIGH issues for best results")
        print("  2. MEDIUM issues are optional but improve output quality")
    else:
        print("  1. Data is ready for document generation")
        print("  2. Review INFO items for awareness")
    print()


def main():
    parser = argparse.ArgumentParser(description="Validate CSV data quality before document generation")
    parser.add_argument("--app-csv", required=True, help="Application portfolio CSV")
    parser.add_argument("--infra-csv", help="Infrastructure inventory CSV (optional)")
    args = parser.parse_args()

    app_rows = read_csv(args.app_csv)
    infra_rows = read_csv(args.infra_csv) if args.infra_csv and os.path.exists(args.infra_csv) else []

    app_issues = validate_apps(app_rows)
    infra_issues = validate_infra(infra_rows) if infra_rows else []

    print_report(app_rows, infra_rows, app_issues, infra_issues)

    # Exit code: 0 if score >= 50, 1 if below
    score = calculate_score(app_issues, infra_issues)
    sys.exit(0 if score >= 50 else 1)


if __name__ == "__main__":
    main()
