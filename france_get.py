import requests

resp = requests.get("https://raw.githubusercontent.com/opencovid19-fr/data/master/dist/chiffres-cles.json")

with open("data/france.json", "w") as file:
    file.write(resp.content.decode("utf-8"))
