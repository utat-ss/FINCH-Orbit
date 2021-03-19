import numpy as np

arr = np.loadtxt("pass.txt", delimiter="    ", skiprows=4, usecols=(2,))
print(arr)
print(np.average(arr))

arr = np.loadtxt("pass550_10.txt", delimiter="    ", skiprows=4, usecols=(2,))
print(arr)
print(np.average(arr))

arr = np.loadtxt("pass500_05.txt", delimiter="    ", skiprows=4, usecols=(2,))
print(arr)
print(np.average(arr))