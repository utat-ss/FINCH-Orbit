from datetime import datetime
import pytz
import pandas
from matplotlib import pyplot as plt
from matplotlib.dates import date2num

eastern = pytz.timezone("Canada/Eastern")

sites = ["Australia",
         "Napanee",
         "Sudbury",
         "Toronto",
         "Windsor",
         "GS"]

encounters = {}

for site in sites:

    with open(f"passes_{site}.txt", "r") as f:
        lines = f.readlines()

        encounters[site] = {"start": [], "end": [], "duration": []}

        for line in lines:

            split = line.split("    ")
            encounters[site]["start"].append(
                eastern.localize(datetime.strptime(split[0], "%d %b %Y %H:%M:%S.%f")))
            encounters[site]["end"].append(
                eastern.localize(datetime.strptime(split[1], "%d %b %Y %H:%M:%S.%f")))
            encounters[site]["duration"].append(float(split[2]))

total = 0
count = 0

for i in range(len(encounters["GS"]["start"])):
    count += 1
    total += encounters["GS"]["duration"][i]

print(total/52)
print(count/52)