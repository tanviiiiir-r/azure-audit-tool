from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network import NetworkManagementClient

def extract_resource_group(resource_id):
    parts = resource_id.split("/")
    return parts[4]

def check_public_storage(credential, subscription_id):
    client = StorageManagementClient(credential, subscription_id)
    result = []

    for account in client.storage_accounts.list():
        rg = extract_resource_group(account.id)
        props = client.storage_accounts.get_properties(rg, account.name)

        print(f"🧪 Checking {account.name} - PublicBlobAccess: {props.allow_blob_public_access}")
        if props.allow_blob_public_access:
            result.append({
                "resource": account.name,
                "issue": "Public blob access enabled",
                "resource_group": rg,
                "severity": "High"
            })
    print(f"✅ check_public_storage found: {result}")
    return result or []

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
                and ("22" in str(rule.destination_port_range) or "22" in (rule.destination_port_ranges or []))
                and ("0.0.0.0/0" in str(rule.source_address_prefix) or "0.0.0.0/0" in (rule.source_address_prefixes or []))
            ):
                rg = extract_resource_group(nsg.id)
                print(f"🚨 NSG {nsg.name} allows SSH from 0.0.0.0/0")
                result.append({
                    "resource": nsg.name,
                    "issue": "SSH port open to the world",
                    "resource_group": rg,
                    "severity": "Critical"
                })
    print(f"✅ check_open_ssh_nsg found: {result}")
    return result or []

def check_open_rdp_nsg(credential, subscription_id):
    client = NetworkManagementClient(credential, subscription_id)
    result = []

    for nsg in client.network_security_groups.list_all():
        rules = nsg.security_rules or []
        for rule in rules:
            if (
                rule.direction == "Inbound"
                and rule.access == "Allow"
                and rule.protocol in ["Tcp", "*"]
                and ("3389" in str(rule.destination_port_range) or "3389" in (rule.destination_port_ranges or []))
                and ("0.0.0.0/0" in str(rule.source_address_prefix) or "0.0.0.0/0" in (rule.source_address_prefixes or []))
            ):
                result.append({
                    "resource": nsg.name,
                    "issue": "RDP port open to the world",
                    "resource_group": extract_resource_group(nsg.id),
                    "severity": "Critical"
                })
    print(f"✅ check_open_rdp_nsg found: {result}")
    return result or []

def check_http_https_open_nsg(credential, subscription_id):
    client = NetworkManagementClient(credential, subscription_id)
    result = []

    for nsg in client.network_security_groups.list_all():
        rules = nsg.security_rules or []
        for rule in rules:
            for port in ["80", "443"]:
                if (
                    rule.direction == "Inbound"
                    and rule.access == "Allow"
                    and rule.protocol in ["Tcp", "*"]
                    and (port in str(rule.destination_port_range) or port in (rule.destination_port_ranges or []))
                    and ("0.0.0.0/0" in str(rule.source_address_prefix) or "0.0.0.0/0" in (rule.source_address_prefixes or []))
                ):
                    result.append({
                        "resource": nsg.name,
                        "issue": f"Port {port} open to the world",
                        "resource_group": extract_resource_group(nsg.id),
                        "severity": "Medium"
                    })
    print(f"✅ check_http_https_open_nsg found: {result}")
    return result or []

def check_https_only_storage(credential, subscription_id):
    client = StorageManagementClient(credential, subscription_id)
    result = []

    for account in client.storage_accounts.list():
        rg = extract_resource_group(account.id)
        props = client.storage_accounts.get_properties(rg, account.name)
        if not props.enable_https_traffic_only:
            print(f"🔴 HTTPS not enforced on {account.name}")
            result.append({
                "resource": account.name,
                "issue": "HTTPS traffic not enforced",
                "resource_group": rg,
                "severity": "High"
            })
    print(f"✅ check_https_only_storage found: {result}")
    return result or []

def check_storage_shared_key_enabled(credential, subscription_id):
    client = StorageManagementClient(credential, subscription_id)
    result = []

    for account in client.storage_accounts.list():
        rg = extract_resource_group(account.id)
        props = client.storage_accounts.get_properties(rg, account.name)
        if props.allow_shared_key_access:
            print(f"⚠️ Shared key access enabled on {account.name}")
            result.append({
                "resource": account.name,
                "issue": "Shared key access enabled",
                "resource_group": rg,
                "severity": "Medium"
            })
    print(f"✅ check_storage_shared_key_enabled found: {result}")
    return result or []
