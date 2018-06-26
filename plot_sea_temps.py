import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap, shiftgrid, cm
%matplotlib inline
import re

def dms2dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    if direction == 'E' or direction == 'N':
        dd *= -1
    return dd;

#import 3D sea surface temp files with lat, lon and depth
tfile = Dataset('/Volumes/Jordan/ANTARCTICA/DATA/woa13_decav_t00_04v2.nc','r')
temp = tfile.variables['t_an'][0,:,0:358,:] # Southern Hemisphere only	
lat = tfile.variables['lat'][0:358] # Southern Hemisphere only
lon = tfile.variables['lon'][:]
dep = tfile.variables['depth'][:]

fig = plt.figure(1)
fig = plt.figure(figsize=[10,10])
fig.patch.set_facecolor('white')
levels1 = np.arange(np.amin(temp),np.amax(temp),.5)
#levels1 = np.arange(1025,1028,.05)
m = Basemap(projection='cyl',llcrnrlon=141,llcrnrlat=-25,urcrnrlon=155,urcrnrlat=-10,resolution='h')
ax1 = fig.add_subplot(111)
m.drawcoastlines()
m.fillcontinents(color='white',lake_color='aqua')
m.drawparallels(np.arange(-80.,81.,1.))
m.drawmeridians(np.arange(-180.,181.,2.))
plt.title('Sea Surface Temperature')
lonp, latp = np.meshgrid(lon,lat)
x, y = m(lonp, latp)
lats=[dms2dd(10,40,55,'N'),dms2dd(10,40,55,'N'),dms2dd(12,59,55,'N'),dms2dd(17,29,55,'N'),dms2dd(20,59,54,'N'),dms2dd(24,29,54,'N'),dms2dd(24,29,54,'N')]
lons=[dms2dd(142.5,0,4,'W'),dms2dd(145,0,4,'W'),dms2dd(145,0,4,'W'),dms2dd(147,0,4,'W'),dms2dd(152,55,4,'W'),dms2dd(154,0,4,'W'),dms2dd(152,0,4,'W')]
m.drawgreatcircle(lons[0],lats[0],lons[1],lats[1],linewidth=1.5,color='k')
m.drawgreatcircle(lons[1],lats[1],lons[2],lats[2],linewidth=1.5,color='k')
m.drawgreatcircle(lons[2],lats[2],lons[3],lats[3],linewidth=1.5,color='k')
m.drawgreatcircle(lons[3],lats[3],lons[4],lats[4],linewidth=1.5,color='k')
m.drawgreatcircle(lons[4],lats[4],lons[5],lats[5],linewidth=1.5,color='k')
m.drawgreatcircle(lons[5],lats[5],lons[6],lats[6],linewidth=1.5,color='k')
CS2 = m.contourf(x, y, temp[0,:,:],cmap= plt.cm.GnBu,extend='both')
cbaxes = fig.add_axes([0.22, 0.13, 0.01, 0.2]) 
plt.colorbar(CS2,cax=cbaxes)  

plt.show()


