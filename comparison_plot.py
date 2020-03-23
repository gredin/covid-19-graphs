import csv
import datetime
import json
from collections import OrderedDict

import matplotlib.pyplot as plt
import numpy as np

min_deaths_sync = 10

# France data

data = json.load(open("data/france.json", "r"))

france_data = OrderedDict()

for d in data:
    if d["code"] != "FRA":
        continue

    sourceType = d["sourceType"]
    if sourceType not in ['sante-publique-france', 'ministere-sante']:
        continue

    date = datetime.datetime.strptime(d["date"], "%Y-%m-%d").date()
    if date not in france_data:
        france_data[date] = None, None, None
    hospitalized_old, icu_old, deaths_old = france_data[date]

    hospitalized = d.get("hospitalises", None)
    icu = d.get("reanimation", None)
    deaths = d.get("deces", None)

    if hospitalized is None:
        hospitalized = hospitalized_old
    elif hospitalized_old is not None and hospitalized_old != hospitalized:
        hospitalized = max(hospitalized_old, hospitalized)

    if icu is None:
        icu = icu_old
    elif icu_old is not None and icu_old != icu:
        icu = max(icu_old, icu)

    if deaths is None:
        deaths = deaths_old
    elif deaths_old is not None and deaths_old != deaths:
        deaths = max(deaths_old, deaths)

    france_data[date] = hospitalized, icu, deaths

# Italie data

data = json.load(open("data/italie.json", "r"))

italie_data = OrderedDict()

for d in data:
    date = datetime.datetime.strptime(d["data"].split(" ")[0], "%Y-%m-%d").date()
    hospitalized = d["ricoverati_con_sintomi"]
    icu = d["terapia_intensiva"]
    deaths = d["deceduti"]

    italie_data[date] = hospitalized, icu, deaths

# Espagne data

espagne_data = OrderedDict()

with open("data/espagne.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    next(csv_reader)

    for row in csv_reader:
        # fecha,casos,altas,fallecimientos,ingresos_uci,hospitalizados

        date = datetime.datetime.strptime(row[0], "%Y-%m-%d").date()

        hospitalized = int(row[5]) if row[5] else None
        icu = int(row[4]) if row[4] else None
        deaths = int(row[3]) if row[3] else None

        espagne_data[date] = hospitalized, icu, deaths

# comparison graph

date_min_france = min([date for date, values in france_data.items() if values[2] and values[2] > min_deaths_sync])
date_min_italie = min([date for date, values in italie_data.items() if values[2] and values[2] > min_deaths_sync])
date_min_espagne = min([date for date, values in espagne_data.items() if values[2] and values[2] > min_deaths_sync])

fig, ax = plt.subplots()
fig.set_size_inches(10, 5)

x = np.array([(date - date_min_france).days for date, values in france_data.items() if date >= date_min_france and values[0] is not None])
y = np.array([values[0] for date, values in france_data.items() if date >= date_min_france and values[0] is not None])
plt.plot(x, y, 'b--', label="France - Hospitalisés")

x = np.array([(date - date_min_france).days for date, values in france_data.items() if date >= date_min_france and values[1] is not None])
y = np.array([values[1] for date, values in france_data.items() if date >= date_min_france and values[1] is not None])
plt.plot(x, y, 'bo', label="France - En réanimation")

x = np.array([(date - date_min_france).days for date, values in france_data.items() if date >= date_min_france and values[2] is not None])
y = np.array([values[2] for date, values in france_data.items() if date >= date_min_france and values[2] is not None])
plt.plot(x, y, 'b:', label="France - Morts")

x = np.array([(date - date_min_italie).days for date, values in italie_data.items() if date >= date_min_italie and values[0] is not None])
y = np.array([values[0] for date, values in italie_data.items() if date >= date_min_italie and values[0] is not None])
plt.plot(x, y, 'g--', label="Italie - Hospitalisés")

x = np.array([(date - date_min_italie).days for date, values in italie_data.items() if date >= date_min_italie and values[1] is not None])
y = np.array([values[1] for date, values in italie_data.items() if date >= date_min_italie and values[1] is not None])
plt.plot(x, y, 'go', label="Italie - En réanimation")

x = np.array([(date - date_min_italie).days for date, values in italie_data.items() if date >= date_min_italie and values[2] is not None])
y = np.array([values[2] for date, values in italie_data.items() if date >= date_min_italie and values[2] is not None])
plt.plot(x, y, 'g:', label="Italie - Morts")

x = np.array([(date - date_min_espagne).days for date, values in espagne_data.items() if date >= date_min_espagne and values[0] is not None])
y = np.array([values[0] for date, values in espagne_data.items() if date >= date_min_espagne and values[0] is not None])
plt.plot(x, y, 'r--', label="Espagne - Hospitalisés")

x = np.array([(date - date_min_espagne).days for date, values in espagne_data.items() if date >= date_min_espagne and values[1] is not None])
y = np.array([values[1] for date, values in espagne_data.items() if date >= date_min_espagne and values[1] is not None])
plt.plot(x, y, 'ro', label="Espagne - En réanimation")

x = np.array([(date - date_min_espagne).days for date, values in espagne_data.items() if date >= date_min_espagne and values[2] is not None])
y = np.array([values[2] for date, values in espagne_data.items() if date >= date_min_espagne and values[2] is not None])
plt.plot(x, y, 'r:', label="Espagne - Morts")

ax.set_xlabel("jours synchronisés (nb. de morts > %s)" % min_deaths_sync)
ax.set_ylabel("nombre de personnes")
ax.set_yscale('log')
ax.set_title("décalage France/Italie : %d jours - décalage Espagne/Italie : %d jours" % ((date_min_france - date_min_italie).days, (date_min_espagne - date_min_italie).days))
plt.legend(loc='best')

plt.show()
fig.savefig("graphs/comparaison.png", dpi=100)
