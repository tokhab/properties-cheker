import json
import zxcvbn
import re
from requests import Request, Session

req = Request('LIST', url="http://172.17.0.2:1234/v1/secret/metadata/", headers={"X-Vault-Token": "myroot"})
prep = req.prepare()
resp = Session().send(prep).text
list_keys = json.loads(resp).get("data").get("keys")

print(list_keys)

for keys in list_keys:
    req_metadata = Request('GET', url="http://172.17.0.2:1234/v1/secret/metadata/%s" % keys, headers={"X-Vault-Token": "myroot"})
    prep_metadata = req_metadata.prepare()
    resp_metadata = Session().send(prep_metadata).text
    keys_metadata = json.loads(resp_metadata).get("data")
    print(keys_metadata['created_time'])
#    json.dumps
    print(keys_metadata)

for keys in list_keys:
    req = Request('GET', url="http://172.17.0.2:1234/v1/secret/data/%s" % keys, headers={"X-Vault-Token": "myroot"})
    prep = req.prepare()
    resp = Session().send(prep).text
    keys_data = json.loads(resp).get("data").get("data")
    print(keys_data)

def check_complexity(password):
    # calculating the length, strong is > 12
    length_error = len(password) < 12
    # searching for digits, strong if 1 digit or more
    digit_error = re.search(r"\d", password) is None
    # searching for uppercase, strong if 1 uppercase letter or more
    uppercase_error = re.search(r"[A-Z]", password) is None
    # searching for lowercase, strong if 1 lowercase letter or more
    lowercase_error = re.search(r"[a-z]", password) is None
    # searching for symbols, strong if 1 symbol or more
    symbol_error = re.search(r"\W", password) is None

    # overall result
    password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)
    stats = zxcvbn(password)

    return {'password_ok': password_ok,
            'length_error': length_error,
            'digit_error': digit_error,
            'uppercase_error': uppercase_error,
            'lowercase_error': lowercase_error,
            'symbol_error': symbol_error,
            'score': stats['score'],
            'guesses': stats['guesses'],
            'entropy': stats['guesses_log10'],
            'crack_times_display': stats['crack_times_display']}