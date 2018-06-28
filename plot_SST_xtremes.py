#!/usr/bin/env python
# -*- coding: utf-8 -*-

# title needs reworking for better understanding of what is represented

"""
Plot SST obs cold and hot extremes for the great barrier reef region,
depending on method to get extreme values

References:
-----------
* netcdf extreme files were generated using CDO ydrunpctl, running mean then
  timpctl, timpctl, yseaspctl, and yearpctl
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
from datetime import date
import matplotlib.pyplot as plt # plotting
import cartopy.crs as ccrs # projection
import cartopy.feature as cfeature # equivalent to basemap

from mhwstats import mhw_stats


#==============================================================================

def main(fname, idate):

	data = read_data(fname)

	if 'ALL' in fname:
		time, __, __ = return_time(data['time'])
		reef_cell = reef_points(data)
		#mhw_stats(time, reef_cell['sst'])
		mhw_stats(time, reef_cell['sst'], coldSpells = True)

	else:
		if '_10_' in fname:
			p_thresh = 10

		if '_90_' in fname:
			p_thresh = 90

		if '_mean_' in fname:
			p_thresh = 0

		if '_seasons.nc' in fname:
			plot_SST_anom(data, p_thresh, idate, seasons = 'yes')

		else:
			plot_SST_anom(data, p_thresh, idate)



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

	ds = xr.open_dataset(fname, drop_variables = ['ice', 'err']) # open .nc
	ds = ds.squeeze(dim = 'zlev', drop = True) # drop elevation var, empty

	return ds


def return_time(xtime):

	start_date = str(xtime[0])
	end_date = str(xtime[len(xtime)-1])
	start_date = (start_date.split('datetime64[ns] ')[1]
				  .split('Attributes:')[0])
	end_date = end_date.split('datetime64[ns] ')[1].split('Attributes:')[0]
	start_date = date(int(start_date[:4]), int(start_date[5:7]),
					  int(start_date[8:10]))
	end_date = date(int(end_date[:4]), int(end_date[5:7]), int(end_date[8:10]))
	time = np.arange(start_date.toordinal(), end_date.toordinal()+1)

	return time, start_date, end_date


def reef_points(data):

	lats = [-10.875, -11.375, -12.125, -13.125, -13.625, -14.375, -15.625, \
			-16.375, -17.375, -18.125, -19.125, -20.125, -21.125, -22.125, \
			-23.625, -24.625]
	lons = [143.125, 143.373, 143.875, 144.375, 144.625, 145.375, 145.625, \
			146.125, 146.375, 146.875, 148.125, 149.625, 150.375, 152.125, \
			152.375, 153.375]

	all_points = data.sel(lon=lons, lat=lats, method='nearest')
	all_points = all_points.mean('lon').mean('lat')

	return all_points


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


def draw_reef(proj):

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
			dms2dd(152, 3, 4, 'W')]
	
	for i in range(len(lats) - 1):

		plt.plot([lons[i], lons[i+1]], [lats[i], lats[i+1]], linewidth = 1.5,
				  color = 'k', transform = proj)

	return


def draw_background_map(ax, lon, lat, proj, res = '10m'):

	ax.set_extent([lon[0], lon[len(lon)-1], lat[0], lat[len(lat)-1]], proj)
	ax.coastlines(resolution = res)
	ax.add_feature(cfeature.LAND, facecolor = 'white')
	ax.add_feature(cfeature.BORDERS, alpha=0.05)

	return


def plot_SST_anom(data, p_thresh, idate, seasons = 'no', layout = 'line',
													 proj = ccrs.PlateCarree()):

	fig = plt.figure()
	fig.patch.set_facecolor('white')

	if layout == 'line':
		ax = plt.subplot(1, 2, 1, projection = proj)

	if layout == 'column':
		ax = plt.subplot(2, 1, 1, projection = proj)

	draw_background_map(ax, data['lon'], data['lat'], proj)
	ctr = ax.contourf(data['lon'], data['lat'], data['sst'][idate,:,:],
					  cmap = plt.cm.GnBu, transform = proj)
	draw_reef(proj)
	fig.colorbar(ctr, ax = ax, fraction = 0.06)
	ax.set_aspect(1.2)
	ax.set_title('SST')

	if layout == 'line':
		ax = plt.subplot(1, 2, 2, projection = proj)

	if layout == 'column':
		ax = plt.subplot(2, 1, 2, projection = proj)

	draw_background_map(ax, data['lon'], data['lat'], proj)
	ctr = ax.contourf(data['lon'], data['lat'], data['anom'][idate,:,:],
					  cmap = plt.cm.GnBu,transform = proj)
	draw_reef(proj)
	fig.colorbar(ctr, ax = ax, fraction = 0.06)
	ax.set_aspect(1.2)
	ax.set_title('SST anomaly')

	# figure title section
	start_date = '1981-09-01'
	end_date = '2018-06-20'

	if seasons == 'yes':
		if idate == 0:
			specify = 'multi-year DJF '

		if idate == 1:
			specify = 'multi-year MAM '

		if idate == 2:
			specify = 'multi-year JJA '

		if idate == 3:
			specify = 'multi-year SON '
		

	if seasons == 'no':
		specify = ''

	if p_thresh == 0:
		fig.suptitle('%smean for %s to %s' % (specify, start_date, end_date))

	else:
		fig.suptitle('%dth %spercentile for %s to %s' % (p_thresh, specify,
					 start_date, end_date))

	namefig = specify.replace(' ', '_')

	if p_thresh == 0:
		namefig += 'mean.png'

	else:
		namefig += '%dth_percentile.png' % (p_thresh)

	namefig = os.path.join(os.getcwd(), 'SST_extremes/%s' % (namefig))
	fig.subplots_adjust(left = 0.075, bottom = 0., top = 1., hspace = 0.1,
						wspace = 0.24)
	plt.tight_layout()
	plt.savefig(namefig, dpi = 1200, transparent = True)


if __name__ == "__main__":

	# if 'SST_ANOM_ALL.nc', mhw is run; if else, plots the representative state
	file = 'SST_90_seasons.nc' # pick a file in SST_extremes/
	#file = 'SST_ANOM_ALL.nc' # pick a file in SST_extremes/

	fname = os.path.join(os.getcwd(), 'SST_extremes') # input data dir path
	fname = os.path.join(fname, file) # full path to file

	idate = 0 # date choice in the timeseries, not relevant for mhw / 'ALL' SST

	main(fname, idate)