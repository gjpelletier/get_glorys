
# ----------
# get_glorys_reanalysis_daily.py 
# 
# Python script to extract daily GLORYS model output
# from the Global Ocean Physics Reanalysis between 1/1/1993 to 12/31/2020
#
# This script is used to download from:

# https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/download?dataset=cmems_mod_glo_phy_my_0.083_P1D-m

# by Greg Pelletier (gjpelletier@gmail.com) (https://github.com/gjpelletier/get_glorys)
# ----------

# - - -
# INSTRUCTIONS
#
# Before using this script, it is first necessary to establish a free account with https://data.marine.copernicus.eu/
# Your username will be assigned when you establish your account. Your password should not include special characters.
#
# After you have established an account, the following are the instructions for using this script:
#
# 1) Edit the user input section below as needed, specify the following:
# 		- list of variables to be extracted from any combination, e.g. var_list = ["so","thetao","uo","vo","zos"]
# 		- west, east, south, and north extent of the bounding box to be extracted
#  		- the name of the OUTPUT_DIRECTORY where the glorys data will be saved as output
# 		- the date_start and number_of_days of the period to be extracted (between 1/1/1993 and 12/31/2020)
# 2) Run this script in python or ipython
# 3) Enter your username and password when prompted
# 4) During execution you sould see the progress of each daily file that is extracted during the period of interest 
#    from beginning to end. Each nc file name has the format glorys_yyyy_MM_dd.nc to indicate the date stamp
#
# - - -
# This python script uses the manual dictionary method that is described at the following Web page:
# https://help.marine.copernicus.eu/en/articles/5211063-how-to-use-the-motuclient-within-python-environment
#
# - - -
# Notes for installing motuclient if you have not yet installed it:
#
#      $ python -m pip install --upgrade motuclient
#   Otherwise (if there is no previous installation of motuclient), 
#   type in the following:
#      $ python -m pip install motuclient
#   That command should install and display motuclient package v1.8.4 (Oct. 2019). 
#   To display the version:
#      $ python -m motuclient --version
#   If that command does not return: "motuclient-python v1.8.X" ("X" >= "4"), 
#   then type in the following:
#     $ python -m pip install motuclient==1.8.4

# - - -
# IMPORT REQUIRED PYTHON PACKAGES

import os
import sys
from datetime import *
import time
from socket import timeout

# aditional packages needed per https://help.marine.copernicus.eu/en/articles/5211063-how-to-use-the-motuclient-within-python-environment:
import getpass
import motuclient

# ----------

# ----------
# ----------
# USER INPUT SECTION

# - - -
# Edit the var_list as needed to download any subset of the available variables listed below:
var_list = ["so","thetao","uo","vo","zos"] 

# any of the following variables may be incuded in var_list:
# so = Seawater salinity [10^-3]
# thetao = Seawater potential temperature [°C]
# uo = Eastward seawater velocity [m/s] 
# vo = Northward seawater velocity [m/s]
# zos = Sea surface height above geoid [m]
# bottomT = sea water potential temperature at sea floor [°C]
# mlotst = Ocean mixed layer thickness defined by sigma theta [m]
# siconc = Sea ice area fraction
# sithick = Sea ice thickness [m]
# usi = Eastward sea ice velocity [m/s]
# vsi = Northward sea ice velocity [m/s]

# specify spatial limits (default below is Parker MacCready's boundary for the boundary of the LiveOcean model):
north = 53              # -90 to 90 degN          
south = 39              # -90 to 90 degN
west = -131             # -180 to 180 or 0 to 360 degE
east = -122             # -180 to 180 or 0 to 360 degE

# -  
# Specify the date_start and number_of_days from 1/1/1993 - 12/31/2020
date_start = '2020-01-01 00:00:00'      # ISO formatted string for the starting datetime for the data to be downloaded (starting hh:mm:ss should be 00:00:00)
number_of_days = 31

# - - -
# specify the directory where the extracted nc files will be saved:
OUTPUT_DIRECTORY = '/mnt/c/data/glorys/daily/'         # include the ending '/'

# END OF USER INPUTS
# ----------
# ----------

# ----------
 
# - - -
# make function to create a directory if it does not already exist
def ensure_dir(file_path):
    # create a folder if it does not already exist
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

# define a class MotuOptions that will be used to parse the motuclient 
class MotuOptions:
    def __init__(self, attrs: dict):
        super(MotuOptions, self).__setattr__("attrs", attrs)

    def __setattr__(self, k, v):
        self.attrs[k] = v

    def __getattr__(self, k):
        try:
            return self.attrs[k]
        except KeyError:
            return None

# - - -
# make function to extract the glorys data during the loop through all datetimes
def get_extraction(dt, data_request_options_dict):
    # get the data and save as a netcdf file
    counter = 1
    got_file = False
    while (counter <= 10) and (got_file == False):
        print('  Attempting to get data, counter = ' + str(counter))
        tt0 = time.time()
        try:
            motuclient.motu_api.execute_request(MotuOptions(data_request_options_dict))
        except timeout:
            print('  *Socket timed out, trying again')
        except:
            print('  *Something went wrong, trying again')      
        else:
            got_file = True
            print('  Downloaded data')
        print('  Time elapsed: %0.1f seconds' % (time.time() - tt0))
        counter += 1
    if got_file:
        result = 'success'
    else:
        result = 'fail'
    return result

# - - -
# make daily dt_list to extract from glorys
base = datetime.fromisoformat(date_start)
ndt = number_of_days
dt_list = []
dt_list = [base + timedelta(hours=24*x) for x in range(ndt)]

# prompt for the user name and password of the user account at https://data.marine.copernicus.eu/products
USERNAME = input('Enter your username: ')
PASSWORD = getpass.getpass('Enter your password: ')

# template dict that will be updated with new dates and output filenames during each iteration of the loop through days
data_request_options_dict_manual = {
    "service_id": "GLOBAL_MULTIYEAR_PHY_001_030-TDS",
    "product_id": "cmems_mod_glo_phy_my_0.083_P1D-m",
    "date_min": " ",
    "date_max": " ",
    "longitude_min": float(west),
    "longitude_max": float(east),
    "latitude_min": float(south),
    "latitude_max": float(north),
    "depth_min": 0.49402499198913574,
    "depth_max": 5727.9169921875,
    "variable": var_list,
    "motu": "https://my.cmems-du.eu/motu-web/Motu",
    "out_dir": OUTPUT_DIRECTORY,
    "out_name": " ",
    "auth_mode": "cas",
    "user": USERNAME,
    "pwd": PASSWORD
}

# - - -
# loop over all datetimes in dt_list
out_dir = OUTPUT_DIRECTORY                   # specify output directory adding the ending '/'
ensure_dir(out_dir)                         # make sure the output directory exists, make one if not
f = open(out_dir + 'log.txt', 'w+')         # open log of successful downloads
print('\n** Working on GLORYS extraction **')
f.write('\n\n** Working on GLORYS extraction **')
tt1 = time.time()                           # tic for total elapsed time
force_overwrite = True                      # overwrite any already existing nc files in the output folder that have the same names
for dt in dt_list:

    out_fn = datetime.strftime(dt, 'glorys_%Y_%m_%d') + '.nc'
    dstr_min = dt.strftime('%Y-%m-%d 00:00:00')
    dstr_max = dt.strftime('%Y-%m-%d 23:59:59')

    data_request_options_dict_manual["out_name"] = out_fn
    data_request_options_dict_manual["date_min"] = dstr_min
    data_request_options_dict_manual["date_max"] = dstr_max

    print(out_dir + out_fn)
    if os.path.isfile(out_fn):
        if force_overwrite:
            os.remove(out_fn)
    if not os.path.isfile(out_fn):
        result = get_extraction(dt, data_request_options_dict_manual)
        f.write('\n ' + datetime.strftime(dt, '%Y_%m_%d') + ' ' + result)
            
# - - -
# final message
totmin = (time.time() - tt1)/60             # total time elapsed for loop over all datetimes in minutes
print('')
print('All downloads are completed.')
print('Total time elapsed: %0.1f minutes' % totmin)
f.close()       # close log of successful downloads


