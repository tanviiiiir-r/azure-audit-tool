#!/bin/bash

echo "🔄 Starting Azure Audit Tool..."
echo "=============================="

# Optional: activate a virtual environment if you use one
# source venv/bin/activate

# Run the main script
python3 main.py

# Show summary
echo ""
echo "📄 Latest Markdown Report (Summary Only):"
echo "----------------------------------------"
grep -A 20 '## 📊 Summary by Severity' reports/audit-report.md

# Optional: open markdown file with default viewer (Mac/Linux)
# xdg-open reports/audit-report.md   # Linux
# open reports/audit-report.md       # macOS

echo ""
echo "✅ Finished! Reports saved in /reports"
