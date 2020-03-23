import csv
import datetime

import matplotlib.pyplot as plt
import numpy as np

min_deaths_country = 100
min_deaths_sync = 20

fixes = [
    # France
    ([6, 9, 11, 19, 19, 33, 48, 48, 79, 91, 91, 148, 148, 148, 243], [5, 9, 11, 19, 30, 33, 48, 61, 79, 91, 127, 148, 175, 244, 372]),

    # Italy
    ([827, 827, 1266], [827, 1016, 1266]),

    # UK
    ([8, 21, 21, 56, 56, 72, 138, 178, 234], [10, 21, 35, 55, 60, 103, 144, 177, 233]),
]

country_deaths = {}

with open("data/countries_deaths.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    first_row = next(csv_reader)
    dates = []
    for d in first_row[4:]:
        month, day, year = d.split("/")
        dates.append(datetime.date(year=int("20" + year), month=int(month), day=int(day)))

    for row in csv_reader:
        country = row[1]

        if country not in country_deaths:
            country_deaths[country] = [0] * len(dates)

        for i, deaths in enumerate([int(deaths or 0) for deaths in row[4:]]):
            country_deaths[country][i] += deaths

for country in country_deaths.keys():
    for before, after in fixes:
        before_str = ",".join(map(str, before))
        after_str = ",".join(map(str, after))

        result = ",".join(map(str, country_deaths[country]))
        result = result.replace(before_str, after_str)
        result = result.split(",")
        result = [int(d) for d in result]

        new_deaths = result
        country_deaths[country] = new_deaths

# morts

last_date_isoformat = dates[-1].isoformat()

fig, ax = plt.subplots()
fig.set_size_inches(20, 10)

for country, deaths in country_deaths.items():
    if deaths[-1] > min_deaths_country:
        deaths_filtered = [d for d in deaths if d > min_deaths_sync]

        # data inconsistencies
        # for i in range(len(deaths_filtered) - 1):
        #    if deaths_filtered[i] == deaths_filtered[i + 1]:
        #        print(country, deaths_filtered[i])

        x = np.array(range(len(deaths_filtered)))
        y = np.array(deaths_filtered)

        plt.plot(x, y, label=country)

ax.set_xlabel("jours synchronisés (nb. de morts > %s)" % min_deaths_sync)
ax.set_ylabel("nombre de personnes")
ax.set_title("morts - %s" % last_date_isoformat)
plt.legend(loc='best')

plt.show()
fig.savefig("graphs/countries_morts_%s.png" % last_date_isoformat, dpi=100)

# par rapport à la veille

fig, ax = plt.subplots()
fig.set_size_inches(10, 5)

for country, deaths in country_deaths.items():
    if country not in ["France", "US", "Italy", "Spain", "Netherlands", "United Kingdom"]:
        continue

    if deaths[-1] > min_deaths_country:
        deaths_filtered = [d for d in deaths if d > min_deaths_sync]

        percentages = []
        for i in range(1, len(deaths_filtered)):
            percentages.append(100 * (deaths_filtered[i] / deaths_filtered[i - 1] - 1))

        x = np.array(range(len(percentages)))
        y = np.array(percentages)

        plt.plot(x, y, label=country)

ax.set_xlabel("jours synchronisés (nb. de morts > %s)" % min_deaths_sync)
ax.set_ylabel("% par rapport à la veille")
ax.set_title("%% de morts par rapport à la veille - %s" % last_date_isoformat)
plt.legend(loc='best')

plt.show()
fig.savefig("graphs/countries_evolution_%s.png" % last_date_isoformat, dpi=100)

# par rapport à la veille, avec lissage

fig, ax = plt.subplots()
fig.set_size_inches(10, 5)

for country, deaths in country_deaths.items():
    if country not in ["France", "US", "Italy", "Spain", "Netherlands", "United Kingdom"]:
        continue

    if deaths[-1] > min_deaths_country:
        deaths_filtered = [d for d in deaths if d > min_deaths_sync]

        percentages = []
        for i in range(2, len(deaths_filtered)):
            ratio = 1 / 2 * (deaths_filtered[i] / deaths_filtered[i - 1] + deaths_filtered[i - 1] / deaths_filtered[i - 2])
            percentages.append(100 * (ratio - 1))

        x = np.array(range(len(percentages)))
        y = np.array(percentages)

        plt.plot(x, y, label=country)

ax.set_xlabel("jours synchronisés (nb. de morts > %s)" % min_deaths_sync)
ax.set_ylabel("% par rapport à la veille")
ax.set_title("%% de morts (avec lissage) par rapport à la veille - %s" % last_date_isoformat)
plt.legend(loc='best')

plt.show()
fig.savefig("graphs/countries_evolution_lissage_%s.png" % last_date_isoformat, dpi=100)
