from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network import NetworkManagementClient

def extract_resource_group(resource_id):
    # Extracts resource group name from Azure resource ID
    parts = resource_id.split("/")
    return parts[4]  # /subscriptions/.../resourceGroups/<name>/...

def check_public_storage(credential, subscription_id):
    client = StorageManagementClient(credential, subscription_id)
    result = []

    for account in client.storage_accounts.list():
        rg = extract_resource_group(account.id)
        props = client.storage_accounts.get_properties(rg, account.name)
        print(f"🧪 Checking {account.name} in {rg} - PublicBlobAccess: {props.allow_blob_public_access}")
        if props.allow_blob_public_access is True:
            result.append({
                "resource": account.name,
                "issue": "Public blob access enabled",
                "resource_group": rg,
                "severity": "High"
            })

    return result or []  # ✅ Ensures we never return None

def check_open_ssh_nsg(credential, subscription_id):
    client = NetworkManagementClient(credential, subscription_id)
    result = []

    for nsg in client.network_security_groups.list_all():
        rules = nsg.security_rules or []
        for rule in rules:
            if (
                rule.direction == "Inbound"
                and rule.access == "Allow"
                and rule.protocol in ["Tcp", "*"]
                and (
                    ("22" in rule.destination_port_range)
                    or ("22" in (rule.destination_port_ranges or []))
                )
                and (
                    rule.source_address_prefix == "0.0.0.0/0"
                    or "0.0.0.0/0" in (rule.source_address_prefixes or [])
                )
            ):
                rg = extract_resource_group(nsg.id)
                print(f"🚨 NSG {nsg.name} allows SSH from 0.0.0.0/0 in {rg}")
                result.append({
                    "resource": nsg.name,
                    "issue": "SSH port open to the world",
                    "resource_group": rg,
                    "severity": "Critical"
                })

    return result or []  # ✅ Prevents 'NoneType' crash
