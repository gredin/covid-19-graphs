import requests

resp = requests.get("https://github.com/pcm-dpc/COVID-19/raw/master/dati-json/dpc-covid19-ita-andamento-nazionale.json")

with open("data/italie.json", "w") as file:
    file.write(resp.content.decode("utf-8"))
