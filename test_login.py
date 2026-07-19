import xmlrpc.client
import getpass

URL = "https://production.misralgadeda.site"
DB = "production"
USER = "aitechpro29@gmail.com"

print("Testing XML-RPC login...")
print("URL :", URL)
print("DB  :", DB)
print("USER:", USER)

password = getpass.getpass("Password: ")

common = xmlrpc.client.ServerProxy(
    f"{URL}/xmlrpc/2/common",
    allow_none=True,
)

print(common.version())

uid = common.authenticate(
    DB,
    USER,
    password,
    {},
)

print("UID:", uid)
