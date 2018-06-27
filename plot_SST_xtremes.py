#!/usr/bin/env python
# -*- coding: utf-8 -*-

# important comment: work in progress, SEASONAL doesn't seem to work
# no idea what the rest is, I will retrieve those extremes using
# a python script tomorrow (or different CDO commands)

"""
Plot SST obs cold and hot extremes for the great barrier reef region,
depending on method to get extreme values

References:
-----------
* netcdf extreme files were generated using CDO ydrunpctl, timpctl,
  yseaspctl, and yearpctl
* original data is NOAA ARVHH daily satellite SST product

"""

__title__ = "Plot various SST extremes"
__version__ = "1.0 (26.06.2018)"
__email__ = "m.e.b.sabot@gmail.com"


#==============================================================================

# general modules
import os, sys # check for files and so on
import xarray as xr # to read netcdf
import numpy as np # data manipulation
import matplotlib.pyplot as plt # plotting
import cartopy.crs as ccrs # projection
import cartopy.feature as cfeature # equivalent to basemap


#==============================================================================

def main(fname):

	data = read_data(fname)
	SST = data['sst']
	anom = data['anom']

	fig, ax = plt.subplots()
	fig.patch.set_facecolor('white')

	ax = plt.subplot(1, 1, 1, projection=ccrs.LambertCylindrical())
	ax.set_extent([data['lon'][0], data['lon'][len(data['lon'])-1],
				  data['lat'][0]-1.25, data['lat'][len(data['lat'])-1]])
	ax.coastlines(resolution = '10m')
	ax.add_feature(cfeature.LAND, facecolor = 'white')
	ax.add_feature(cfeature.BORDERS, alpha=0.05)

	ctr = plt.contourf(data['lon'], data['lat'], data['sst'][0,:,:],
		   			  cmap = plt.cm.GnBu,transform = ccrs.LambertCylindrical())
	draw_reef()
	plt.colorbar(ctr)

	fig.suptitle('Sea Surface Temperature')
	plt.show()



#==============================================================================

def read_data(fname):

	"""
	Reads netcdf file and returns the dataset containing only relevant vars

	Arguments:
	----------
	fname: string
		input filename (with path)

	Returns:
	--------
	ds: xarray dataset
		contains the sst and anom data

	"""

	ds = xr.open_dataset(fname, drop_variables = ['ice', 'err']) # access the data
	ds = ds.squeeze(dim = 'zlev', drop = True) # drop elevation var, empty

	return ds


def dms2dd(degrees, minutes, seconds, direction):

	"""
	Converts input geo coordinate into convention format
 
	Arguments:
	----------
	degrees: int or float

	minutes: int or float

	seconds: int or float

	direction: string
		'N', 'W', 'S', 'E'

	Returns:
	--------
	dd: float
		conventional expression of the coordinate

	"""

	dd = float(degrees) + float(minutes) / 60. + float(seconds) / (60. * 60.)

	if direction == 'E' or direction == 'N':
		dd *= -1

	return dd


def draw_reef():

	"""
	Adds the reef's boundaries to the map

	"""

	lats = [dms2dd(10, 40, 55, 'N'), dms2dd(10, 40, 55, 'N'), \
			dms2dd(12, 59, 55, 'N'), dms2dd(17, 29, 55, 'N'), \
			dms2dd(20, 59, 54, 'N'), dms2dd(24, 29, 54, 'N'), \
			dms2dd(24, 29, 54, 'N')]

	lons = [dms2dd(142.5, 0, 4, 'W'), dms2dd(145, 0, 4, 'W'), \
			dms2dd(145, 0, 4, 'W'), dms2dd(147, 0, 4, 'W'), \
			dms2dd(152, 55, 4, 'W'), dms2dd(154, 0, 4, 'W'), \
			dms2dd(152, 52, 4, 'W')]
	
	for i in range(len(lats) - 1):

		plt.plot([lons[i], lons[i+1]], [lats[i], lats[i+1]],
				 linewidth = 1.5, color = 'k',
        		 transform = ccrs.LambertCylindrical())

	return


if __name__ == "__main__":

	fname = os.path.join(os.getcwd(), 'SST_extremes') # input data dir path
	fname = os.path.join(fname, 'SST_90_yrs_20rm.nc')

	main(fname)