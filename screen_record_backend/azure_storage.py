import os
from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):
    account_name = os.getenv('AZURE_ACCOUNT_NAME', 'sanctus')
    account_key = os.getenv('AZURE_ACCOUNT_KEY', 'Y0Z6u6g+QW9+9Y4qI9fJg8M4gJX9fQ2X3yF4l7q7l3w==')
    azure_container = 'media'
    expiration_secs = None


class AzureStaticStorage(AzureStorage):
    account_name = os.getenv('AZURE_ACCOUNT_NAME', 'sanctus')
    account_key = os.getenv('AZURE_ACCOUNT_KEY', 'Y0Z6u6g+QW9+9Y4qI9fJg8M4gJX9fQ2X3yF4l7q7l3w==')
    azure_container = 'static'
    expiration_secs = None
