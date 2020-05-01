#!/usr/bin/python3

import sys
import re
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as mt
import pandas as pd
import numpy as np

# Heat index coefficients
HI_COEF = np.array([[-8.784695, 1.61139411, 2.338549, -0.14611605, -1.2308094e-2, -1.6424828e-2, 2.211732e-3, 7.2546e-4, -3.582e-6]])

# Calculates the head index from temperature and humidity
def add_heat_index(df):
    x = [[1,
          r.temperature,
          r.humidity,
          r.temperature * r.humidity,
          pow(r.temperature, 2),
          pow(r.humidity, 2),
          pow(r.temperature, 2) * r.humidity,
          r.temperature * pow(r.humidity, 2),
          pow(r.temperature, 2) * pow(r.humidity, 2)
         ] for _, r in df.iterrows()]
    df['heatindex'] = np.matmul(np.array(x), HI_COEF.T)

# Remove outliers 
# (data points with values that are n times larger 
# the difference to the previous data point in time)
def reject_outliers(data, m=3):
    n = len(data)
    diffs = [abs(data[i] - data[i-1]) for i in range(1, n)]
    diffs = [diffs[0]] + diffs
    return diffs > m * np.median(diffs)

### Main ###

filename = sys.argv[1]

# Read CSV and set columns
df = pd.read_csv(filename, sep='\t', header=None, index_col=None)
df.columns = ('timestamp', 'temperature', 'humidity', 'pressure')

# Convert timestamp to suitable data type for filtering
dates = [datetime.fromtimestamp(ts) for ts in df.timestamp]
df['timestamp'] = dates
df['year'] = [d.year for d in dates]
df['month'] = [d.month for d in dates]
df['day'] = [d.day for d in dates]
df['hour'] = [d.hour for d in dates]
df['minute'] = [d.minute for d in dates]

# Reject outliers
outliers = reject_outliers(df.temperature).tolist()
outliers = np.any([outliers, reject_outliers(df.humidity).tolist()], axis=0)
outliers = np.any([outliers, reject_outliers(df.pressure).tolist()], axis=0)
df.drop(df.index[outliers], inplace=True)

add_heat_index(df)

# Plot and save different graphs in one image
time_formatter = md.DateFormatter("%Y-%m-%d %H:%M")

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(12,8))
ax[0, 0].plot_date(pd.to_datetime(df.timestamp), df.temperature, '-', color='blue')
ax[1, 0].plot_date(pd.to_datetime(df.timestamp), df.heatindex, '-', color='brown')
ax[0, 1].plot_date(pd.to_datetime(df.timestamp), df.humidity, '-', color='orange')
ax[1, 1].plot_date(pd.to_datetime(df.timestamp), df.pressure, '-', color='green')
ax[0, 0].set_title('Temperature (°C)')
ax[1, 0].set_title('Heat index (°C)')
ax[0, 1].set_title('Relative humidity (%)')
ax[1, 1].set_title('Barometric pressure (hPa)')

for r in [0, 1]:
    for c in [0, 1]:
        ax[r, c].grid(True)
        ax[r, c].yaxis.set_major_formatter(mt.FormatStrFormatter('%.1f'))
        ax[r, c].xaxis.set_major_formatter(time_formatter)
        ax[r, c].xaxis.set_major_locator(plt.MaxNLocator(10))

ax[0, 0].xaxis.set_ticklabels([])
ax[0, 1].xaxis.set_ticklabels([])
plt.sca(ax[1, 0])
plt.xticks(rotation=45, ha='right')
plt.sca(ax[1, 1])
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('graph.png', bbox_inches='tight')


