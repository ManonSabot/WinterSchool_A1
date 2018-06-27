Numbers 10 and 90 indicate the 10th percentile (cold) and 90th percentile (hot) of SST. \
The seasons files show the percentiles seasonally \
Files with _yr.nc show the percentiles across all years (several dates) \
Files with _yrs.nc show a single value which I think is the average of all dates falling in the 10th or 90th category \
Files with _20rm.nc show the dates in the middle of the 20 day window, same as _yrs.nc, but the original data is smoothed over a 20 day running mean period \
Files with _20rp.nc show the dates in the middle of the 20 day window for a running percentile over the whole time series

Can do more tomorrow...
To have a look, use plot_SST_xtremes.py
