from azure.identity import AzureCliCredential
from azure.keyvault.secrets import SecretClient

from pybehave.utils.assertutils import Assert


class KeyvaultReader:
    """
    Keyvault reader class
    """

    def get_keyvault_client(self, kv_uri):
        """get the key vault client"""
        try:
            credential = AzureCliCredential()
            return SecretClient(vault_url=kv_uri, credential=credential)
        except Exception as ex:
            Assert.assert_fail(f"Unable to resolve the KeyVault url - '{kv_uri}' : {ex}")
