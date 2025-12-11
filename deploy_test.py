import requests
r = requests.get("https://cloud.therink.io/api/v1/teams", headers={"Authorization": "Bearer 2|1AVWKq6jqYmnCH5TFtHnYPrGGC0HuNZGOH2sy3b0deb49e23"})
print(r.json())
