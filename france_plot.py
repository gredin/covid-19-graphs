import datetime
import json
from collections import OrderedDict

import matplotlib.pyplot as plt
import numpy as np

data = json.load(open("data/france.json", "r"))

hospitalized_data = OrderedDict()
icu_data = OrderedDict()
deaths_data = OrderedDict()

for d in data:
    if d["code"] != "FRA":
        continue

    sourceType = d["sourceType"]

    if sourceType not in ['sante-publique-france', 'ministere-sante']:
        continue

    date = datetime.datetime.strptime(d["date"], "%Y-%m-%d").date()

    hospitalized = d.get("hospitalises", None)
    icu = d.get("reanimation", None)
    deaths = d.get("deces", None)

    if hospitalized is not None:
        old_count = hospitalized_data.get(date, None)

        if old_count is not None and old_count != hospitalized:
            print("erreur", date, old_count, hospitalized)
            hospitalized = max(old_count, hospitalized)

        hospitalized_data[date] = hospitalized

    if icu is not None:
        old_count = icu_data.get(date, None)

        if old_count is not None and old_count != icu:
            print("erreur", date, old_count, icu)
            icu = max(old_count, icu)

        icu_data[date] = icu

    if deaths is not None:
        old_count = deaths_data.get(date, None)

        if old_count is not None and old_count != deaths:
            print("erreur", date, old_count, deaths)
            deaths = max(old_count, deaths)

        deaths_data[date] = deaths

print(hospitalized_data)
print(icu_data)
print(deaths_data)

# nombre de personnes

fig, ax = plt.subplots()
fig.set_size_inches(10, 5)

x = np.array([date for date, _ in hospitalized_data.items()])
y = np.array([v for _, v in hospitalized_data.items()])
plt.plot(x, y, label="Hospitalisés")

x = np.array([date for date, _ in icu_data.items()])
y = np.array([v for _, v in icu_data.items()])
plt.plot(x, y, label="En réanimation")

x = np.array([date for date, _ in deaths_data.items()])
y = np.array([v for _, v in deaths_data.items()])
plt.plot(x, y, label="Morts")

ax.set_xlabel("jours")
ax.set_ylabel("nombre de personnes")
ax.set_title("personnes hospitalisées / en réanimation / mortes - France")
plt.legend(loc='best')

plt.show()
fig.savefig("graphs/france.png", dpi=100)

# par rapport à la veille

min_date = min([date for date, _ in hospitalized_data.items()] +
               [date for date, _ in icu_data.items()] +
               [date for date, _ in deaths_data.items()])
max_date = max([date for date, _ in hospitalized_data.items()] +
               [date for date, _ in icu_data.items()] +
               [date for date, _ in deaths_data.items()])

hospitalized_pourcentages = []
icu_pourcentages = []
deaths_pourcentages = []

date = datetime.date(year=2020, month=3, day=5)  # min_date
while date <= max_date:
    day_before = date - datetime.timedelta(days=1)

    if day_before in hospitalized_data and date in hospitalized_data and hospitalized_data[day_before] > 0:
        hospitalized_pourcentages.append((date, 100 * (hospitalized_data[date] / hospitalized_data[day_before] - 1)))

    if day_before in icu_data and date in icu_data and icu_data[day_before] > 0:
        icu_pourcentages.append((date, 100 * (icu_data[date] / icu_data[day_before] - 1)))

    if day_before in deaths_data and date in deaths_data and deaths_data[day_before] > 0:
        deaths_pourcentages.append((date, 100 * (deaths_data[date] / deaths_data[day_before] - 1)))

    date = date + datetime.timedelta(days=1)

fig, ax = plt.subplots()
fig.set_size_inches(10, 5)

x = np.array([date for date, _ in hospitalized_pourcentages])
y = np.array([v for _, v in hospitalized_pourcentages])
plt.plot(x, y, label="Hospitalisés")

x = np.array([date for date, _ in icu_pourcentages])
y = np.array([v for _, v in icu_pourcentages])
plt.plot(x, y, label="En réanimation")

x = np.array([date for date, _ in deaths_pourcentages])
y = np.array([v for _, v in deaths_pourcentages])
plt.plot(x, y, label="Morts")

ax.set_xlabel("jours")
ax.set_ylabel("% par rapport à la veille")
ax.set_title("% par rapport à la veille - France")
plt.legend(loc='best')

plt.show()
fig.savefig("graphs/france_evolution.png", dpi=100)
