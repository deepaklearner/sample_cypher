File
Edit Format View Help
import smtplib
from email.mime.application import MIMEApplication from email.mime.multipart import MIMEMultipart from email.mime.text import MIMElext from email.utils import formataddr from email.header import Header
from os.path import basename from os import remove import yaml import argparse import glod
Import logging
from retrieve_azure_creds import read_secrets_from_keyvault
def read creds(configstream):
Read Credentlals
Cry:
secret reader=read secrets from keyvault(configstream)
data=secret_reader.read_secret_from_keyvault
except Exception as e:
logging info"Exception occurrec at get credentials: ", e)
return data
class mail server:
def
init_(self, configfile, notification_log_location):
try:
with open (configfile, 'r') as file:
self.config=yaml.safe_load(file)
for key in self.config.keys:
1og files=lfile for file in glob.globnotification log location+key+ /*')J
if len(log files>0 and self.config key is enabled ==Y:
self.mail server=mail config 'MAIL SERVER'] self.mail port=mail config MAIL PORT' self.mail_from=mail config 'MAIL FROM']
self.mail sender name=mail config MAIL SENDER NAME
self.mail_to=list(map(str. strip, mail_config[ MAIL_TO']. split(*')))
selt.mail subject=self.config key 'MAIL SUBJECT'] self.mail_text=self.config[key]['MAIL_TEXT']
self.send mail(log files)
logging.info Email Alert Sent to Techops Team") for file in log files:
remove tile)
except Exception as e:
logging-errorf"|ERROR] - Email Notification Process Failed, Please Debug ‹ utils/techops_load _alert.py> | Error: (e)
det send mailself,files=None):
message-MiMeMultiparto
message | 'FROM =formataddrstr Header(self.mail sender name, utf-8',self.mail from
messagel lo=,
". join (self.mail to)
messagel subject=self.mail subiect message.attachMIMETextself.mail text))
for file in files:
with open(file, rb' as f:
part = MIMEApplication(f.read),Name = basename (file) replace (FULL, WARNINGS))
part ['Content-Disposition'] = 'attachment; filename="%"*% basename(file). replace'FULL', 'WARNINGS')
message.aruach part)
server = smtplib.SMTP(self.mail server,self.mail port)
server. sendmall (self.mall from,
seit-mall_to, message.as_string())
server.quit()

if __name__='__main__':
mann
parser = argparse. ArgumentParser(description="Email logs")
parser.add argument ("config file",nargs='?',default= 'config/config-yaml, help="Location of config-yaml") parser.add_argument log_file, help="Specify the Log file where logs will be captured for delta sync")
args = parser.parse args)
contig = args.config file
parser = argparse.ArgumentParser(description="Full and Delta Synchronization")

# Setting up logging
logging.basicconfig(Tilename=args.log_file, level=logging.N-0,
format-"%(asctime)s %(message)s', datefmt=^%Y-%m-%d %H:%M:%5' )
_sdk_loggen = logging-getLogger ('azure')
azure_sak_logger.setLevel (logging.WARNING)
# Read database credentials from do_credentials. yaml
with open(config, "r") as stream_data:
try:
configstream=yaml.safe_load（stream_data)
database_configs = read_creds (configstream)
mail_config = database_configs.get ('MailServer', (})
mail_server (configstream[ 'notification_config'], configstream[ 'notification _1og_location'])
except Exception as e:
logging-error (str(e))
