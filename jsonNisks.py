import json
users_nicks = {}
with open ("Nicks.json", "w", encoding="utf8") as f :
    json.dump (users_nicks, f, indent=4, ensure_ascii=False)