import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.interpolate import interpn

img = Image.open("Earth_Diffuse_6K.jpg")
imgdata = np.asarray(img)

factor = 60

lats = np.linspace(0, np.pi, int(imgdata.shape[0]/factor)) # this is actually latitude + 90
lons = np.linspace(0, 2*np.pi, int(imgdata.shape[1]/factor))

LATS, LONS = np.meshgrid(lats, lons)

values = interpn((lats, lons), imgdata[::factor, ::factor, :], (LATS.ravel(), LONS.ravel()))


X = np.sin(LATS)*np.cos(LONS)
Y = np.sin(LATS)*np.sin(LONS)
Z = np.cos(LATS)
x = X.ravel()
y = Y.ravel()
z = Z.ravel()


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Create cubic bounding box to simulate equal aspect ratio
max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max()
Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(X.max()+X.min())
Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(Y.max()+Y.min())
Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(Z.max()+Z.min())
# Comment or uncomment following both lines to test the fake bounding box:
for xb, yb, zb in zip(Xb, Yb, Zb):
   ax.plot([xb], [yb], [zb], 'w')

ax.scatter(x, y, z, c=values/255)
plt.show()