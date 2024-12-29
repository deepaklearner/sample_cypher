from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import requests
import socket
import re
import yaml

class ReadSecretsFromKeyVault:
    def __init__(self, configuration_file):
        self.config_file = configuration_file
        self.server_creds = yaml.safe_load(open(self.config_file, 'r'))
        self.keyvault_uri = self.server_creds["KeyvaultURI"]
        self.ne04j_config = self.server_creds["NE04"]
        
        # Request to get region information
        region = requests.get(
            "http://169.254.169.254/metadata/instance/compute/location?api-version=2021-02-01&format=text",
            headers={'Metadata': 'true'}
        ).text
        
        # Get hostname of the instance
        hostname = socket.gethostname()
        
        # Set vault URI based on hostname and region
        if re.search(r'dl\d', hostname):
            self.vault_uri = self.keyvault_uri["dev_keyvault_uri"]
        elif re.search(r'ul\d', hostname) and re.search(r'east', region):
            self.vault_uri = self.keyvault_uri["uat_east_keyvault_uri"]
        elif re.search(r'ul\d', hostname) and re.search(r'central', region):
            self.vault_uri = self.keyvault_uri["uat_central_keyvault_uri"]
        elif re.search(r'pl\d', hostname) and re.search(r'east', region):
            self.vault_uri = self.keyvault_uri["prod_east_keyvault_uri"]
        elif re.search(r'pl\d', hostname):
            self.vault_uri = self.keyvault_uri["prod_keyvault_uri"]
    
    def read_secret_from_keyvault(self):
        vault_url = f"https://{self.vault_uri}.vault.azure.net"
        credential = DefaultAzureCredential()
        secret_client = SecretClient(vault_url=vault_url, credential=credential)
        
        # Read content from configuration file
        with open(self.config_file, 'r') as file:
            content = file.read()
        
        # Pattern to find the upstream values in the content
        pattern = r'(Upstream[0-9a-zA-Z-]+)'
        vars = re.findall(pattern, content)
        
        try:
            for var in vars:
                # Retrieve the secret value from Azure Key Vault
                secret_value = secret_client.get_secret(var).value
                content = content.replace(var, secret_value)
            
            # Parse updated content into YAML
            data = yaml.safe_load(content)
            return data
        
        except Exception as e:
            print(f"Error: {e}")
