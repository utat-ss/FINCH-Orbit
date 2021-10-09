import numpy as np
import plotly.graph_objects as go
import numpy as np
from PIL import Image
from scipy.interpolate import interpn

img = Image.open("Earth_Diffuse_6K.jpg")
imgdata = np.asarray(img)

factor = 30

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


fig = go.Figure(data=[go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='markers',
    marker=dict(
        size=5,
        color=values
    )
)])

# tight layout
fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
# fig.show()

fig.write_html("file.html")