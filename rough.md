from azure identity import DefaultAzureCredential from
azure. keyvault secrets import Secretclient
import requests import socket import re import
ou, 6 days ago | 2 authors (ghp_M2WD4vqUaRf1Fbpj9sL5zPAQhRb5A3wt6kx and one other)
class read_secrets_from_keyvault:
def
-init_(self, configuration file):
self.config_file - configuration_file
self.server_creds - yaml. safe_load(open(self config_file,'r*))
self.keyvault_uri - self.server_creds["KeyvaultURI']
self.ne04j_config - self.server_creds["NE04]']
region=requests-get(http://169.254.169.254/metadata/instance/compute/location?api
hostname-socket-gethostname()
-version=2021-02-01&format-text*
, headers={'Metadata': 'true'}).text
if re.search(r*dl\d',hostname):
self.vaulturi-self.keyvault_uri["dev_keyvaulturi"]
if re.search(r'ul\d', hostname)
and re. search(r'east*,region):
self.vaulturi-self.keyvault_uri["uat_east_keyvaulturi"]
if research(r'ul\d'
, hostname
and re.search(r'central',region):
self-vaulturi-self.keyvault_uri["uat_central_keyvaulturi"]
if re.search(r'pl\d*,hostname)
and re.search(r'east'
, region):
self.vaulturi=self.keyvault_uri["prod
_east_keyvaulturi"]
if re.search(r'pl\d*
, hostname)
def
read_secret_ from_keyvault(self):
vault_url - f"https://{self.vaulturif.vault.azure.net/*
credential = DefaultAzureCredential()
secret_client = Secretclient(vault_url-vault_url,
credential-credential)
with open(self.config_file,'r') as file:
content-file.read
pattern-r' (Upstream[0-9a-ZA-Z-]+)
vars=re.findall (pattern, content) try:
i in vars:
secret value - secret_client-get_secret(1)-value content=content.replace(1, secret_value)
data-yaml.safe_load(content)
return data except Exception
as
print (f"Error:
{e}"D