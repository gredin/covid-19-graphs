import requests

resp = requests.get("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv")

with open("data/countries_deaths.csv", "w") as csv_file:
    csv_file.write(resp.content.decode("utf-8"))
