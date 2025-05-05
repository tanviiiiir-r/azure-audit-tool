from azure.identity import AzureCliCredential
from azure.mgmt.resource import SubscriptionClient

def get_credentials():
    credential = AzureCliCredential()
    subscription_client = SubscriptionClient(credential)
    subscription = next(subscription_client.subscriptions.list())
    return credential, subscription.subscription_id
