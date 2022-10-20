import requests as r
import json

# keep the field 'n' and 'l' of orgas.json from code.gouv
with open("orgas.json", "r") as f:
    orgas = json.load(f)
to_match_str = []
for org in orgas:
   to_match_str.append(org["n"])
   to_match_str.append(org["l"])

to_match_str = [s.lower() if type(s)==str else s for s in to_match_str]
url = "https://hub.docker.com/v2/orgs/"
found = dict()

# check if ther there is a public orga account associated to these names
for k, s in enumerate(to_match_str):
    if k == (len(to_match_str) - 1) or k%100==0:
        print(f"{1+k}/{len(to_match_str)}")
    resp = r.get(url+s)
    try:
        resp = resp.json()
        if (resp["is_active"] and resp["orgname"]):
            found[resp["orgname"]] = {"name": resp["full_name"], "since":resp["date_joined"], "url": resp["profile_url"], "service": resp["company"]}
    except Exception as e:
        pass

with open("hubdocker_accounts.json", "w") as f:
   json.dump(found, f)
