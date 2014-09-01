# -*- coding: utf-8 -*-
"""
This will DESTROY ALL YOUR DATA.....

looks for netCDF files  - and then trys to 'clean' them...
INPLACE...
WITHOUT BACKUPS...

Created on Sat Jul 26 19:47:19 2014
@author: ran110
"""

'change me to whatever is the error'
magicErrorNumber = -1.401298464324817e-45

import netCDF4
import glob
import numpy as np


fileList = sorted(glob.glob('*.nc4'))

for currentFile in fileList:
    print 'Current File - ', currentFile
    error = False
    dataSet = netCDF4.Dataset(currentFile, 'r+', format='NETCDF4')
    elevation = dataSet.variables['elevation']
    if 'cleaned' not in elevation.ncattrs():
        print elevation.shape

        for i in range(0, elevation.shape[0], 5000):
            numbers = elevation[i:i+5000]
            if np.any(numbers==magicErrorNumber):
                try:
                    numbers[np.isclose(numbers, magicErrorNumber)] = np.nan
                    elevation[i:i+5000]=numbers
                    elevation.errors="True"
                    print "...errors found"
                except:
                    pass

        print ' - cleaning complete'
        elevation.cleaned="True"
    else:
        print ' - already cleaned'

    if 'vrs' not in elevation.ncattrs() or elevation.vrs != '"http://www.opengis.net/def/crs/epsg/0/5711"':
        print '''said who? how do you know it is this?'''
        elevation.vrs = '"http://www.opengis.net/def/crs/epsg/0/5711"'
    else:
        print 'already in there....'


    dataSet.close()

