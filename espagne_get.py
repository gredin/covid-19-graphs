import requests

resp = requests.get("https://github.com/datadista/datasets/raw/master/COVID%2019/nacional_covid19.csv")
with open("data/espagne.csv", "w") as file:
    file.write(resp.content.decode("utf-8"))
