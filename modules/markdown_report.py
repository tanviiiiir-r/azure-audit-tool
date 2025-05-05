def generate_markdown_report(issues):
    from collections import Counter

    # Group issues by severity
    severity_counts = Counter(issue["severity"] for issue in issues)

    # Create Markdown output
    markdown = "# 🔐 Azure Cloud Audit Report\n\n"
    markdown += "## 📊 Summary by Severity\n\n"
    markdown += "| Severity  | Count |\n"
    markdown += "|-----------|-------|\n"
    for severity, count in severity_counts.items():
        markdown += f"| {severity:<9} | {count:<5} |\n"

    markdown += "\n## 📋 Detailed Issues\n\n"
    markdown += "| Resource               | Issue                          | Resource Group                  | Severity  |\n"
    markdown += "|------------------------|--------------------------------|----------------------------------|-----------|\n"
    for issue in issues:
        markdown += (
            f"| {issue['resource']:<22} "
            f"| {issue['issue']:<30} "
            f"| {issue['resource_group']:<32} "
            f"| {issue['severity']:<9} |\n"
        )

    # Save markdown file
    with open("reports/audit-report.md", "w") as f:
        f.write(markdown)

    print("✅ Markdown report saved: reports/audit-report.md")

    return markdown

