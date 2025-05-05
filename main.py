from modules.auth import get_credentials
from modules.misconfig_checks import check_public_storage, check_open_ssh_nsg
from modules.report_generator import save_report
from modules.markdown_report import generate_markdown_report

def main():
    print("✅ Script started")

    credential, sub_id = get_credentials()
    print(f"🔐 Subscription ID: {sub_id}")

    issues = []
    issues.extend(check_public_storage(credential, sub_id))
    issues.extend(check_open_ssh_nsg(credential, sub_id))

    print(f"🧾 Issues found: {issues}")

    if issues:
        save_report(issues)
        
        # ✅ Save Markdown version too
        md_report = generate_markdown_report(issues)
        with open("reports/audit-report.md", "w") as f:
            f.write(md_report)
        print("📝 Markdown report saved: reports/audit-report.md")

if __name__ == "__main__":
    main()
