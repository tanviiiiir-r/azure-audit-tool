# 🔐 Azure Cloud Audit Report

## 📊 Summary by Severity

| Severity  | Count |
|-----------|-------|
| High      | 2     |
| Critical  | 1     |
| Medium    | 3     |

## 📋 Detailed Issues

| Resource               | Issue                          | Resource Group                  | Severity  |
|------------------------|--------------------------------|----------------------------------|-----------|
| auditstorage0110081    | Public blob access enabled     | cloud-shell-storage-westeurope   | High      |
| auditVM01NSG           | SSH port open to the world     | cloud-shell-storage-westeurope   | Critical  |
| rdp-test-nsg           | Port 80 open to the world      | cloud-shell-storage-westeurope   | Medium    |
| rdp-test-nsg           | Port 443 open to the world     | cloud-shell-storage-westeurope   | Medium    |
| auditstorage0110081    | HTTPS traffic not enforced     | cloud-shell-storage-westeurope   | High      |
| auditstorage0110081    | Shared key access enabled      | cloud-shell-storage-westeurope   | Medium    |
