from modules.auth import get_credentials
from modules.misconfig_checks import (
    check_public_storage,
    check_open_ssh_nsg,
    check_open_rdp_nsg,
    check_http_https_open_nsg,
    check_https_only_storage,
    check_storage_shared_key_enabled
)
from modules.report_generator import save_report
from modules.markdown_report import generate_markdown_report

def main():
    print("✅ Script started")

    credential, sub_id = get_credentials()
    print(f"🔐 Subscription ID: {sub_id}")

    issues = []

    print("🔍 Running: check_public_storage")
    issues.extend(check_public_storage(credential, sub_id))

    print("🔍 Running: check_open_ssh_nsg")
    issues.extend(check_open_ssh_nsg(credential, sub_id))

    print("🔍 Running: check_open_rdp_nsg")
    issues.extend(check_open_rdp_nsg(credential, sub_id))

    print("🔍 Running: check_http_https_open_nsg")
    issues.extend(check_http_https_open_nsg(credential, sub_id))

    print("🔍 Running: check_https_only_storage")
    issues.extend(check_https_only_storage(credential, sub_id))

    print("🔍 Running: check_storage_shared_key_enabled")
    issues.extend(check_storage_shared_key_enabled(credential, sub_id))

    print(f"🧾 Total issues found: {len(issues)}")

    if issues:
        save_report(issues)
        md_report = generate_markdown_report(issues)
        with open("reports/audit-report.md", "w") as f:
            f.write(md_report)
        print("📝 Markdown report saved: reports/audit-report.md")
    else:
        print("✅ No misconfigurations found!")

if __name__ == "__main__":
    main()
