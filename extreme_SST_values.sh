#!/bin/bash

#------------------------------------------------------------------------------
# Purpose:
# Extract SST cold and hot extremes, arbritrarily defined as the 10th and 90th
# percentiles of SST. These can be looked at over a multi-year (with or
# without running options), multi-year seasonal, or yearly period.
#
# You might have to run:
# sed -i -e 's/\r$//' extreme_SST_values.sh
# to make the script compliant across all linux systems
#
# Contact: manon sabot <m.e.b.sabot@gmail.com>
#------------------------------------------------------------------------------


# multi year with 20 days running percentile
cdo ydrunmin,20 ./SST_ANOM_ALL.nc minfile.nc
cdo ydrunmax,20 ./SST_ANOM_ALL.nc maxfile.nc
cdo ydrunpctl,10,20 ./SST_ANOM_ALL.nc ./minfile.nc ./maxfile.nc \
	./SST_10_yrs_20rp.nc
cdo ydrunpctl,90,20 ./SST_ANOM_ALL.nc ./minfile.nc ./maxfile.nc \
	./SST_90_yrs_20rp.nc
rm ./minfile.nc ./maxfile.nc


# multi year with 20 days running mean
cdo runmean,20 ./SST_ANOM_ALL.nc runmean.nc
cdo timmin ./runmean.nc minfile.nc
cdo timmax ./runmean.nc maxfile.nc
cdo timpctl,10 ./runmean.nc ./minfile.nc ./maxfile.nc \
	./SST_10_yrs_20rm.nc
cdo timpctl,90 ./runmean.nc ./minfile.nc ./maxfile.nc \
	./SST_90_yrs_20rm.nc
rm ./runmean.nc ./minfile.nc ./maxfile.nc


# multi year no running mean
cdo timmin ./SST_ANOM_ALL.nc minfile.nc
cdo timmax ./SST_ANOM_ALL.nc maxfile.nc
cdo timpctl,10 ./SST_ANOM_ALL.nc ./minfile.nc ./maxfile.nc \
	./SST_10_yrs.nc
cdo timpctl,90 ./SST_ANOM_ALL.nc ./minfile.nc ./maxfile.nc \
	./SST_90_yrs.nc
rm ./minfile.nc ./maxfile.nc


# multi year across seasons
cdo yseasmin ./SST_ANOM_ALL.nc minfile.nc
cdo yseasmax ./SST_ANOM_ALL.nc maxfile.nc
cdo yseaspctl,10 ./SST_ANOM_ALL.nc ./minfile.nc ./maxfile.nc \
	./SST_10_seasons.nc
cdo yseaspctl,90 ./SST_ANOM_ALL.nc ./minfile.nc ./maxfile.nc \
	./SST_90_seasons.nc
rm ./minfile.nc ./maxfile.nc


# for comparaison, multi-year seasonal mean
cdo yseasmean ./SST_ANOM_ALL.nc ./SST_mean_seasons.nc

# each year
cdo yearpctl,10 ./SST_ANOM_ALL.nc -yearmin ./SST_ANOM_ALL.nc \
	-yearmax ./SST_ANOM_ALL.nc ./SST_10_yr.nc
cdo yearpctl,90 ./SST_ANOM_ALL.nc -yearmin ./SST_ANOM_ALL.nc \
	-yearmax ./SST_ANOM_ALL.nc ./SST_90_yr.nc
