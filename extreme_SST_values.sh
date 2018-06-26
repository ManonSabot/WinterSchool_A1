#!/bin/bash

#------------------------------------------------------------------------------
# Purpose:
# Extract SST cold and hot extremes, arbritrarily defined as the 10th and 90th
# percentiles of SST. These can be looked at over a multi-year (with or)
# without running mean), multi-year seasonal, or yearly period.
#
# You might have to run:
# sed -i -e 's/\r$//' extreme_SST_values.sh
# to make the script compliant across all linux systems
#
# Contact: manon sabot <m.e.b.sabot@gmail.com>
#------------------------------------------------------------------------------


# multi year with 20 days running mean
cdo ydrunmin,20 ./SST_ANOM_ALL.nc minfile.nc
cdo ydrunmax,20 ./SST_ANOM_ALL.nc maxfile.nc
cdo ydrunpctl,10,20 ./SST_ANOM_ALL.nc ./minfile.nc ./maxfile.nc \
	./SST_10_yrs_20rm.nc
cdo ydrunpctl,90,20 ./SST_ANOM_ALL.nc ./minfile.nc ./maxfile.nc \
	./SST_90_yrs_20rm.nc
rm ./minfile.nc ./maxfile.nc


# multi year no running mean
cdo timpctl,10 ./SST_ANOM_ALL.nc -timmin ./SST_ANOM_ALL.nc \
	-timmax ./SST_ANOM_ALL.nc ./SST_10_yrs.nc
cdo timpctl,90 ./SST_ANOM_ALL.nc -timmin ./SST_ANOM_ALL.nc \
	-timmax ./SST_ANOM_ALL.nc ./SST_90_yrs.nc


# multi year across seasons
cdo yseaspctl,10 ./SST_ANOM_ALL.nc -seasmin ./SST_ANOM_ALL.nc \
	-seasmax ./SST_ANOM_ALL.nc ./SST_10_seasons.nc
cdo yseaspctl,90 ./SST_ANOM_ALL.nc -seasmin ./SST_ANOM_ALL.nc \
	-seasmax ./SST_ANOM_ALL.nc ./SST_90_seasons.nc


# each year
cdo yearpctl,10 ./SST_ANOM_ALL.nc -yearmin ./SST_ANOM_ALL.nc \
	-yearmax ./SST_ANOM_ALL.nc ./SST_10_yr.nc
cdo yearpctl,90 ./SST_ANOM_ALL.nc -yearmin ./SST_ANOM_ALL.nc \
	-yearmax ./SST_ANOM_ALL.nc ./SST_90_yr.nc
