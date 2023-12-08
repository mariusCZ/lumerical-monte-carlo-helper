import numpy as np
import configparser as cg
from shapely.geometry import Point, Polygon
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

config = cg.ConfigParser()
config.read('config.ini')

lumpath = config['COMMON']['lum_path']
if not lumpath:
    raise ValueError('Lumerical API path is empty, please update it in config.ini!')

filepath = config['MONTE_GENERATION']['filepath']
if not filepath:
    raise ValueError('No basis file path provided, please update it in config.ini!')
outpath = config['MONTE_GENERATION']['outpath']
outname = config['MONTE_GENERATION']['outname']
if not outname:
    outname = "monte"

x = config['MONTE_GENERATION']['x']
if not x:
    raise ValueError('No x points provided, please update it in config.ini!')
y = config['MONTE_GENERATION']['y']
if not y:
    raise ValueError('No y points provided, please update it in config.ini!')

phi_bnd = config['MONTE_GENERATION']['phi_bnd']
if not phi_bnd:
    raise ValueError('No phi boundaries provided, please update it in config.ini!')
else:
    phi_bnd = [float(i) for i in phi_bnd.split(',')]
phi_rot = config['MONTE_GENERATION']['phi_rot']
if not phi_rot:
    raise ValueError('No setting for random phi rotation provided, please update it in config.ini!')
phi = config['MONTE_GENERATION']['phi']
if not phi:
    raise ValueError('No default phi provided, please update it in config.ini!')

src = config['MONTE_GENERATION']['src_name']
if not src:
    raise ValueError('No source name provided, please update it in config.ini!')

num = config['MONTE_GENERATION']['num']
if not num:
    raise ValueError('No number of simulations provided, please update it in config.ini!')


import importlib.util
spec_lin = importlib.util.spec_from_file_location('lumapi', lumpath)
# spec_lin = importlib.util.spec_from_file_location('lumapi', "D:/Software/Lumerical/api/python/lumapi.py")
lumapi = importlib.util.module_from_spec(spec_lin)
spec_lin.loader.exec_module(lumapi)

def Random_Points_in_Bounds(polygon, number):   
    minx, miny, maxx, maxy = polygon.bounds
    x = np.random.uniform( minx, maxx, number )
    y = np.random.uniform( miny, maxy, number )
    return x, y

x = [float(i) for i in x.split(',')]
y = [float(i) for i in y.split(',')]
xy = list(zip(x, y))
polygon = Polygon(xy)
gdf_poly = gpd.GeoDataFrame(index=["myPoly"], geometry=[polygon])

x,y = Random_Points_in_Bounds(polygon, 10_000)
df = pd.DataFrame()
df['points'] = list(zip(x,y))
df['points'] = df['points'].apply(Point)
gdf_points = gpd.GeoDataFrame(df, geometry='points')

Sjoin = gpd.tools.sjoin(gdf_points, gdf_poly, predicate="within", how='left')

# Keep points in "myPoly"
pnts_in_poly = gdf_points[Sjoin.index_right=='myPoly']
x = [i['geometry']['coordinates'][0] for i in pnts_in_poly.iterfeatures()]
y = [i['geometry']['coordinates'][1] for i in pnts_in_poly.iterfeatures()]
x = x[:int(num)]
y = y[:int(num)]
plt.plot(x, y, 'bo')
plt.show()

with lumapi.FDTD(filename=filepath, hide=True) as fdtd:
    for i in range(int(num)):
        fdtd.select(src)
        fdtd.set("x", x[i]*1e-6)
        fdtd.set("y", y[i]*1e-6)
        if phi_rot == '1':
            fdtd.set("phi", np.random.uniform(phi_bnd[0], phi_bnd[1]))
        else:
            fdtd.set("phi", int(phi))
        fdtd.save(outpath+outname+'_'+str(i)+".fsp")
