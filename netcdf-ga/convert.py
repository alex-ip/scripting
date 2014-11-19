# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 13:09:56 2014

@author: ran110
"""
import os, subprocess

'''gdal_translate w001001.adf -of netCDF -co FORMAT=NC4C -co COMPRESS=DEFLATE ~/BremerBasin-50m-WGS84UTM50S.nc4
'''
gdal_command = ['gdal_translate', \
                '-of', 'netCDF', \
                '-co', 'FORMAT=NC4C', \
                '-co', 'COMPRESS=DEFLATE',
                '-co', 'WRITE_BOTTOMUP=YES', ]
'''
ncrename -v Band1,elevation busselton-final.nc
ncatted -h -O -a long_name,elevation,o,c,elevation busselton-final.nc
ncatted -h -O -a  positive,elevation,a,c,"up" busselton-final.nc
ncatted -h -O -a  units,elevation,a,c,"http://www.opengis.net/def/uom/OGC/1.0/metre" busselton-final.nc
ncatted -h -O -a  vrs,elevation,a,c,"http://www.opengis.net/def/crs/epsg/0/5711" busselton-final.nc
'''
inPlaceCleanup = [
            ['ncrename', '-v', 'Band1,elevation', ], \
            ['ncatted', '-h', '-O', '-a', 'long_name,elevation,o,c,elevation', ], \
            ['ncatted', '-h', '-O', '-a', 'positive,elevation,a,c,"up"', ], \
            ['ncatted', '-h', '-O', '-a', 'units-uri,elevation,a,c,"http://www.opengis.net/def/uom/OGC/1.0/metre"', ], \
            ['ncatted', '-h', '-O', '-a', 'units-uri,elevation,a,c,"metre"', ], \
            ['ncatted', '-h', '-O', '-a', 'vrs-uri,elevation,a,c,"http://www.opengis.net/def/crs/EPSG/0/5773"', ], \
            ['ncatted', '-h', '-O', '-a', 'vrs,elevation,a,c,"EGM96"', ], \
          ]

outputdir = "/g/data1/rr1/conversions/newconvert"

for root, subFolders, files in os.walk("/g/data1/rr1/Elevation/1secSRTM_DEMs_v1.0/"):
    if 'prj.adf' in files:
        inputfile = root

        prettyname = root.replace("/g/data1/rr1/","").replace("/","_").replace(" ", "_") + '.nc'
        outputfullname = outputdir + os.path.sep + prettyname
        if os.path.isfile(outputfullname):
            continue
        
        print gdal_command + [inputfile, outputfullname]
        subprocess.check_call(gdal_command + [inputfile, outputfullname])
        for operation in inPlaceCleanup:
            print operation + [outputfullname]
            subprocess.check_call(operation + [outputfullname])
        subprocess.check_call(['nccopy', '-d', '2', '-c', 'lat/128,lon/128', outputfullname,  outputfullname+'.128-128.nc'])
