while installing python-ldap i am getting below error:
could not fetch url https://pypi.org/simple/setuptools.: there was  problem confirming the ssl certificate

my os is red hat enterprise linux 8.10(ootpa) x86_64

temp solution:
python3 -m pip install python-ldap --trusted-host pypi.org --trusted-host pypi.python.org

even after adding --trusted-host  i am getting error could not fetch url https://pypi.org/simple/setuptools/: there was problem confirming ssl certificate

error occured in violation of protocol (_ssl.c:1131)