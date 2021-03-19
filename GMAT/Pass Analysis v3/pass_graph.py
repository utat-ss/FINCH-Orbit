from datetime import datetime
import pytz
from matplotlib import pyplot as plt
from matplotlib.dates import date2num
from matplotlib.widgets import Slider, Button, RadioButtons

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

        encounters[site] = {"start": [], "end": []}

        for line in lines:

            split = line.split("    ")
            encounters[site]["start"].append(
                eastern.localize(datetime.strptime(split[0], "%d %b %Y %H:%M:%S.%f")))
            encounters[site]["end"].append(
                eastern.localize(datetime.strptime(split[1], "%d %b %Y %H:%M:%S.%f")))


def timelines(y, xstart, xstop, color='b'):
    """Plot timelines at y from xstart to xstop with given color."""   
    plt.hlines(y, xstart, xstop, color, lw=8)
    plt.vlines(xstart, y+0.4, y-0.4, color, lw=2)
    plt.vlines(xstop, y+0.4, y-0.4, color, lw=2)


y = 1

for site in encounters:
    start = date2num(encounters[site]["start"])
    stop = date2num(encounters[site]["end"])

    #Plot ok tl black    
    for i in range(len(start)):
        timelines(y, start[i], stop[i], 'b')

    y += 1

#Setup the plot
ax = plt.gca()
ax.xaxis_date()

#To adjust the xlimits a timedelta is needed.
delta = (stop.max() - start.min()) # total range
plt.ylim(0,7)
plt.xlim(start.min(), start.min() + 30)

plt.yticks(range(1, 7), sites)
plt.xlabel('Time')



plt.show()