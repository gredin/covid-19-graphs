import datetime
import json

import matplotlib.pyplot as plt
import numpy as np

data = json.load(open("data/italie.json", "r"))

processed_data = []

for day_data in data:
    date = datetime.datetime.strptime(day_data["data"].split(" ")[0], "%Y-%m-%d").date()
    hospitalized = day_data["ricoverati_con_sintomi"]
    icu = day_data["terapia_intensiva"]
    deaths = day_data["deceduti"]

    processed_data.append((date, hospitalized, icu, deaths))

hospitalized = [hospitalized for _, hospitalized, _, _ in processed_data]
icu = [icu for _, _, icu, _ in processed_data]
deaths = [deaths for _, _, _, deaths in processed_data]

hospitalized_pourcentages = [100 * (hospitalized[i + 1] / hospitalized[i] - 1) for i in range(len(hospitalized) - 1)]
icu_pourcentages = [100 * (icu[i + 1] / icu[i] - 1) for i in range(len(icu) - 1)]
deaths_pourcentages = [100 * (deaths[i + 1] / deaths[i] - 1) for i in range(len(deaths) - 1)]

# optim

# hospitalized = [hospitalized[i] for i in range(len(hospitalized) - 1)]
# icu = [icu[i] for i in range(len(icu) - 1)]
# deaths_new = [deaths[i + 1] - deaths[i] for i in range(len(deaths) - 1)]

input = icu_pourcentages
output = deaths_pourcentages

erreurs_to_be_sorted = []
for decalage in range(15):
    for proportion in [x / 500 for x in range(0, 500)]:
        predictions = [None for _ in output]

        for i, _ in enumerate(predictions):
            if i + decalage >= len(predictions):
                continue

            predictions[i + decalage] = proportion * input[i]

        errs = []
        for i, _ in enumerate(predictions):
            if predictions[i] is None:
                continue

            err = predictions[i] - output[i]  # /output[i]
            errs.append(abs(err))

        err_moyenne = sum(errs) / len(errs)

        erreurs_to_be_sorted.append((err_moyenne, decalage, proportion, predictions))

erreurs_sorted = sorted(erreurs_to_be_sorted, key=lambda e: e[0])

print(erreurs_sorted[:10])

print(output)

# nombre de personnes

fig, ax = plt.subplots()
fig.set_size_inches(10, 5)

x = np.array([date for date, _, _, _ in processed_data])

y = np.array(hospitalized)
plt.plot(x, y, label="Hospitalisés")

y = np.array(icu)
plt.plot(x, y, label="En réanimation")

y = np.array(deaths)
plt.plot(x, y, label="Morts")

ax.set_xlabel("jours")
ax.set_ylabel("nombre de personnes")
ax.set_title("personnes hospitalisées / en réanimation / mortes - Italie")
plt.legend(loc='best')

plt.show()
fig.savefig("graphs/italie.png", dpi=100)

# par rapport à la veille

fig, ax = plt.subplots()
fig.set_size_inches(10, 5)

x = np.array([date for date, _, _, _ in processed_data][1:])

y = np.array(hospitalized_pourcentages)
plt.plot(x, y, label="Hospitalisés")

y = np.array(icu_pourcentages)
plt.plot(x, y, label="En réanimation")

y = np.array(deaths_pourcentages)
plt.plot(x, y, label="Morts")

ax.set_xlabel("jours")
ax.set_ylabel("% par rapport à la veille")
ax.set_title("% par rapport à la veille - Italie")
plt.legend(loc='best')

plt.show()
fig.savefig("graphs/italie_evolution.png", dpi=100)
