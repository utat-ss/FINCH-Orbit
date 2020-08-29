from numpy import sin, cos, tan, arctan
import numpy as np

from datetime import datetime

from matplotlib import pyplot as plt
from matplotlib import dates
import matplotlib.ticker as ticker

starts = []
### Data Link
with open("torontodata.txt", "r") as f:
    for line in f.readlines()[1:50]:
        line = line.strip("\n").split("    ") 
        starts.append(datetime.strptime(line[0], "%d %b %Y %H:%M:%S.%f"))

starts = dates.date2num(starts)

yeet = 2*np.ones(len(starts))

fig, ax = plt.subplots()



plt.plot_date(starts, yeet, "|",label="Data Link", markersize=20)

starts = []
### Import File
with open("nadirimaging.txt", "r") as f:
    for line in f.readlines()[1:20]:
        line = line.strip("\n").split("    ") 
        starts.append(datetime.strptime(line[0], "%d %b %Y %H:%M:%S.%f"))

starts = dates.date2num(starts)

yeet = 3*np.ones(len(starts))

plt.plot_date(starts, yeet,"|", label="Nadir Imaging", markersize=20)

starts = []
### Import File
with open("ttc.txt", "r") as f:
    for line in f.readlines()[1:100]:
        line = line.strip("\n").split("    ") 
        starts.append(datetime.strptime(line[0], "%d %b %Y %H:%M:%S.%f"))

starts = dates.date2num(starts)

yeet = 1*np.ones(len(starts))

plt.plot_date(starts, yeet,"|", label="TT & C", markersize=20)

starts = []
### Import File
with open("limbimaging.txt", "r") as f:
    for line in f.readlines()[1:150]:
        line = line.strip("\n").split("    ") 
        starts.append(datetime.strptime(line[0], "%d %b %Y %H:%M:%S.%f"))
        starts.append(datetime.strptime(line[1], "%d %b %Y %H:%M:%S.%f"))

starts = dates.date2num(starts)

yeet = 4*np.ones(len(starts))

plt.plot_date(starts, yeet,"|", label="Limb Imaging", markersize=20)

plt.legend(loc="upper left")

plt.grid(True)

fig.subplots_adjust(bottom=0.3)
plt.xticks(rotation=90)

plt.ylim(0, 5)

plt.show()