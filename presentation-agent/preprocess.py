"""CSV Preprocessor — converts raw application and infrastructure CSVs into structured context for the Presentation Agent.

Usage:
    python3.11 preprocess.py --app-csv portfolio.csv --infra-csv servers.csv --output context.md
    python3.11 preprocess.py --app-csv portfolio.csv --infra-csv servers.csv --scope scope.txt --output context.md

Then feed into the presentation agent:
    python3.11 presentation_agent.py --type executive_summary --context-file context.md
"""

import argparse
import csv
import os
import sys
from collections import Counter


def read_csv(path: str) -> list[dict]:
    """Read CSV file, handling BOM, quoting, and flexible delimiters."""
    with open(path, "r", encoding="utf-8-sig") as f:
        content = f.read()
    # Strip BOM and clean up quoted headers
    content = content.lstrip("\ufeff")
    # Detect delimiter
    delimiter = "," if content.count(",") > content.count("\t") else "\t"
    reader = csv.DictReader(content.splitlines(), delimiter=delimiter, quotechar='"', skipinitialspace=True)
    # Clean field names and values
    rows = []
    for row in reader:
        cleaned = {k.strip().strip('"'): v.strip().strip('"') if v else "" for k, v in row.items() if k}
        rows.append(cleaned)
    return rows


def analyse_apps(rows: list[dict]) -> str:
    """Analyse application portfolio and return markdown summary."""
    total = len(rows)
    if total == 0:
        return "No application data provided.\n"

    # Detect column names (flexible matching)
    def find_col(row, candidates):
        for c in candidates:
            for key in row.keys():
                if c.lower() in key.lower():
                    return key
        return None

    sample = rows[0]
    name_col = find_col(sample, ["App_Name", "Application Name", "Name", "app_name"])
    crit_col = find_col(sample, ["Criticality", "SLA_Tier", "Priority"])
    type_col = find_col(sample, ["App_Category", "App_Type", "Type", "Category"])
    lang_col = find_col(sample, ["Primary_Language", "Technology Stack", "Language", "Tech"])
    db_col = find_col(sample, ["Database", "Database_Dependencies", "DB"])
    env_col = find_col(sample, ["Environment", "Env"])
    strategy_col = find_col(sample, ["Recommended Strategy", "Strategy", "R_Type"])
    wave_col = find_col(sample, ["Migration Wave", "Wave"])

    lines = []
    lines.append(f"## Application Portfolio Summary\n")
    lines.append(f"- **Total applications:** {total}")

    # Criticality distribution
    if crit_col:
        crit_counts = Counter(row.get(crit_col, "Unknown").strip() for row in rows)
        lines.append(f"- **Criticality distribution:**")
        for level, count in sorted(crit_counts.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"  - {level}: {count}")

    # Type distribution
    if type_col:
        type_counts = Counter(row.get(type_col, "Unknown").strip() for row in rows)
        lines.append(f"- **Application types:**")
        for t, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"  - {t}: {count}")

    # Environment distribution
    if env_col:
        env_counts = Counter(row.get(env_col, "Unknown").strip().upper() for row in rows)
        lines.append(f"- **Environments:** {', '.join(f'{k}: {v}' for k, v in env_counts.items())}")

    # 6Rs distribution
    if strategy_col:
        strat_counts = Counter(row.get(strategy_col, "Unknown").strip() for row in rows)
        lines.append(f"\n### 6Rs Distribution")
        for s, count in sorted(strat_counts.items(), key=lambda x: x[1], reverse=True):
            pct = round(count / total * 100)
            lines.append(f"- {s}: {count} ({pct}%)")

    # Wave plan
    if wave_col:
        wave_counts = Counter(row.get(wave_col, "N/A").strip() for row in rows)
        lines.append(f"\n### Wave Plan")
        for w, count in sorted(wave_counts.items()):
            lines.append(f"- {w}: {count} applications")

    # Technology landscape
    if lang_col:
        all_tech = []
        for row in rows:
            tech = row.get(lang_col, "")
            all_tech.extend([t.strip() for t in tech.replace("|", "/").split("/") if t.strip()])
        tech_counts = Counter(all_tech)
        lines.append(f"\n### Technology Landscape (Top 10)")
        for tech, count in tech_counts.most_common(10):
            lines.append(f"- {tech}: {count} apps")

    # Risk signals (EOL detection)
    eol_keywords = ["java 8", "java 6", "java 7", "cobol", ".net 4", "asp.net 4", "python 2", "vb6", "weblogic 12"]
    eol_apps = []
    if lang_col:
        for row in rows:
            tech = row.get(lang_col, "").lower()
            for kw in eol_keywords:
                if kw in tech:
                    eol_apps.append((row.get(name_col, "Unknown"), kw))
                    break
    if eol_apps:
        lines.append(f"\n### EOL/Legacy Risk Signals")
        for app, signal in eol_apps:
            lines.append(f"- **{app}**: {signal}")

    # Application table
    lines.append(f"\n### Application Details")
    cols = [c for c in [name_col, crit_col, type_col, lang_col, strategy_col, wave_col] if c]
    if cols:
        lines.append("| " + " | ".join(cols) + " |")
        lines.append("| " + " | ".join(["---"] * len(cols)) + " |")
        for row in rows:
            lines.append("| " + " | ".join(row.get(c, "—") for c in cols) + " |")

    return "\n".join(lines)


def analyse_infra(rows: list[dict]) -> str:
    """Analyse infrastructure inventory and return markdown summary."""
    total = len(rows)
    if total == 0:
        return "No infrastructure data provided.\n"

    sample = rows[0]

    def find_col(row, candidates):
        for c in candidates:
            for key in row.keys():
                if c.lower() in key.lower():
                    return key
        return None

    name_col = find_col(sample, ["Server Name", "server_name", "Hostname"])
    cpu_col = find_col(sample, ["CPU", "cpu_cores", "vCPU"])
    mem_col = find_col(sample, ["Memory", "RAM", "mem"])
    storage_col = find_col(sample, ["Storage", "Disk", "Provisioned"])
    os_col = find_col(sample, ["Operating System", "OS", "os_name"])
    env_col = find_col(sample, ["Environment", "Env"])
    type_col = find_col(sample, ["Workload Type", "Type", "Role"])
    virtual_col = find_col(sample, ["Virtual", "Is Virtual", "is_virtual"])

    lines = []
    lines.append(f"\n## Infrastructure Summary\n")
    lines.append(f"- **Total components:** {total}")

    # Environment split
    if env_col:
        env_counts = Counter(row.get(env_col, "Unknown").strip().upper() for row in rows)
        lines.append(f"- **By environment:** {', '.join(f'{k}: {v}' for k, v in env_counts.items())}")

    # Workload types
    if type_col:
        type_counts = Counter(row.get(type_col, "Unknown").strip() for row in rows)
        lines.append(f"- **Workload types:**")
        for t, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"  - {t}: {count}")

    # Total resources
    if cpu_col:
        total_cpu = sum(int(row.get(cpu_col, 0) or 0) for row in rows if str(row.get(cpu_col, "")).isdigit())
        lines.append(f"- **Total vCPU:** {total_cpu}")
    if mem_col:
        total_mem = sum(int(row.get(mem_col, 0) or 0) for row in rows if str(row.get(mem_col, "")).replace(".", "").isdigit())
        lines.append(f"- **Total Memory:** {total_mem:,} MB ({total_mem // 1024:,} GB)")
    if storage_col:
        total_storage = sum(float(row.get(storage_col, 0) or 0) for row in rows if str(row.get(storage_col, "")).replace(".", "").isdigit())
        lines.append(f"- **Total Storage:** {total_storage:,.0f} GB ({total_storage / 1024:,.0f} TB)")

    # OS distribution
    if os_col:
        os_counts = Counter(row.get(os_col, "Unknown").strip() for row in rows)
        lines.append(f"\n### Operating Systems")
        for o, count in os_counts.most_common(10):
            lines.append(f"- {o}: {count}")

    # Infrastructure table
    lines.append(f"\n### Infrastructure Details")
    cols = [c for c in [name_col, cpu_col, mem_col, storage_col, os_col, env_col, type_col] if c]
    if cols:
        lines.append("| " + " | ".join(cols) + " |")
        lines.append("| " + " | ".join(["---"] * len(cols)) + " |")
        for row in rows:
            lines.append("| " + " | ".join(str(row.get(c, "—")) for c in cols) + " |")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Convert CSVs to structured context for the Presentation Agent")
    parser.add_argument("--app-csv", required=True, help="Application portfolio CSV")
    parser.add_argument("--infra-csv", help="Infrastructure inventory CSV (optional)")
    parser.add_argument("--scope", help="Scope/drivers text file (optional)")
    parser.add_argument("--customer", default="Customer", help="Customer name")
    parser.add_argument("--partner", default="Partner", help="Partner name")
    parser.add_argument("--output", required=True, help="Output context markdown file")
    args = parser.parse_args()

    sections = []
    sections.append(f"# Migration Context — {args.customer}\n")
    sections.append(f"- **Customer:** {args.customer}")
    sections.append(f"- **Partner:** {args.partner}")
    sections.append("")

    # Scope file
    if args.scope and os.path.exists(args.scope):
        with open(args.scope, "r") as f:
            sections.append("## Scope and Migration Drivers\n")
            sections.append(f.read().strip())
            sections.append("")

    # Application portfolio
    app_rows = read_csv(args.app_csv)
    sections.append(analyse_apps(app_rows))

    # Infrastructure
    if args.infra_csv and os.path.exists(args.infra_csv):
        infra_rows = read_csv(args.infra_csv)
        sections.append(analyse_infra(infra_rows))

    output = "\n".join(sections)
    with open(args.output, "w") as f:
        f.write(output)
    print(f"Context generated: {args.output} ({len(output):,} chars, {len(app_rows)} apps", end="")
    if args.infra_csv:
        print(f", {len(infra_rows)} infra components", end="")
    print(")")


if __name__ == "__main__":
    main()
