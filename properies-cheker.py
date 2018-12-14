import json
import requests
from requests import Request, Session

req = Request('LIST', url="http://172.17.0.2:1234/v1/secret/metadata/", headers={"X-Vault-Token": "myroot"})
prep = req.prepare()
resp = Session().send(prep).text
list_keys = json.loads(resp).get("data").get("keys")

for x in list_keys:
    req = Request('GET', url="http://172.17.0.2:1234/v1/secret/metadata/%s" % x, headers={"X-Vault-Token": "myroot"})
    prep = req.prepare()
    resp = Session().send(prep).text
    list_keys = json.loads(resp).get("data")
    print(type(list_keys))
    print(list_keys)