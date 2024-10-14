From azure.identity import DefaultAzureCredential from azure.keyvault.secrets import SecretClient import requests import socket import re import yaml
class read_ secrets from_keyvault:
def
init
_(self, configstream) :
region=requests get 'http://169.254.169.254/metadata/instance/compute/location?api-version=2021-02-01&format=text' ,headers={ 'Metadata': 'true'}). text hostname-socket-gethostname )
self.configstream=configstream if re. search(r'dl\d',hostname) :
self.vaulturi=self.configstream["dev_keyvaulturi"
if re. search(r'ul\d',hostname)
and
re. search(r'east' ,region):
self.vaulturi-self.configstream["uat_ east_keyvaulturi"]
if re.search(r'ul\d*,hostname) and
re.search(r'central",region):
self.vaulturi-self.configstream["uat_central_keyvaulturi"]
if re.search(r'pl\d'
, hostname) and re-search(r'east', region):
self.vaulturi-self.configstream[*prod_
east_keyvaulturi"]
if re.search(r'pl\d*,hostname)
and re search(r"central'
, region) :
self.vaulturi-self.configstream["prod_central_keyvaulturi"l
def read_secret_from_keyvault(self):
vault url - f"https://{self.vaulturi}.vault.azure.net/*
credential - DefaultAzureCredential()
secret_client - SecretClient(vault_url-vault_url, credential-credential) with open(self.configstream[*db_crendentials_file'],'r*) as file:
content-file.read)
pattern=r' (Upstream[0-9a-zA-Z-]+) *
#pattern=r' (Upstream[0-9a-zA-Z-]+ |SMTP-MAIL [0-9a-zA-Z-]+) *
vars=re. findall(pattern, content)
for i in vars:
secret_value - secret_client get_secreti) .value content-content. replace(i, secret_value)
data-yaml. safe_load(content)
return data
except Exception as e:
print(f"Error: {e)")