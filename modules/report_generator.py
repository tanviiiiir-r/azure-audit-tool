import os
import json
from datetime import datetime

def save_report(issues):
    try:
        # Make sure the reports folder exists
        os.makedirs("reports", exist_ok=True)

        # Delete all old audit reports before saving the new one
        for file in os.listdir("reports"):
            if file.startswith("audit-report-") and file.endswith(".json"):
                os.remove(os.path.join("reports", file))

        # Save the new report
        filename = f"reports/audit-report-{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        with open(filename, "w") as f:
            json.dump(issues, f, indent=4)
        print(f"✅ New report saved: {filename}")
    except Exception as e:
        print(f"❌ Failed to save report: {e}")
