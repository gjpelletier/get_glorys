
# ----------
# get_glorys_forecast_biogeochem_monthly.py 
# 
# Python script to extract monthly GLORYS model output
# from the Global Ocean Biogeochemistry Analysis and Forecast between 11/2020 to present
#
# This script is used to download from:

# https://data.marine.copernicus.eu/product/GLOBAL_ANALYSIS_FORECAST_BIO_001_028/download

# by Greg Pelletier | gjpelletier@gmail.com | https://github.com/gjpelletier/get_glorys
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
# 		- list of variables to be extracted from any combination, e.g. var_list = ["dissic","talk","si","po4","ph","spco2","o2","no3","fe","phyc","chl","nppv"] 
# 		- west, east, south, and north extent of the bounding box to be extracted
#  		- the name of the OUTPUT_DIRECTORY where the glorys data will be saved as output
# 		- the date_start and number_of_months of the period to be extracted (between 11/1/2020 to present)
#       - the min and max depths (dep_min and dep_max) (between 0 and 5728m)
# 2) Run this script in python or ipython
# 3) Enter your username and password when prompted
# 4) During execution you sould see the progress of each monthly file that is extracted during the period of interest 
#    from beginning to end. Each nc file name has the format glorys_biogeochem_yyyy_MM.nc to indicate the date stamp
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
from dateutil.relativedelta import relativedelta
import calendar     # calendar.monthrange(year, month) returns weekday (0-6 ~ Mon-Sun) and number of days (28-31) for year, month.

# aditional packages needed per https://help.marine.copernicus.eu/en/articles/5211063-how-to-use-the-motuclient-within-python-environment:
import getpass
import motuclient

# ----------

# ----------
# ----------
# USER INPUT SECTION

# - - -
# specify the directory where the extracted nc files will be saved:
OUTPUT_DIRECTORY = '/mnt/c/data/glorys/forecast_monthly/'         # include the ending '/'

# - - -
# Edit the var_list as needed to download any subset of the available variables listed below:
var_list = ["dissic","talk","si","po4","ph","spco2","o2","no3","fe","phyc","chl","nppv"] 

# any of the following variables may be incuded in var_list:
# dissic = Mole concentration of dissolved inorganic carbon in sea water [mol/m3]
# talk = Sea water alkalinity expressed as mole equivalent [mol/m3]
# si = Mole concentration of silicate in sea water [mmol/m3]
# po4 = Mole concentration of phosphate in sea water [mmol/m3]
# ph = Sea water pH reported on total scale
# spco2 = Surface partial pressure of carbon dioxide in sea water [Pa]
# o2 = Mole concentration of dissolved molecular oxygen in sea water [mmol/m3]
# no3 = Mole concentration of nitrate in sea water [mmol/m3]
# fe = Mole concentration of dissolved iron in sea water [mmol/m3] 
# phyc = Mole concentration of phytoplankton expressed as carbon in sea water [mmol/m3]
# chl = Mass concentration of chlorophyll a in sea water [mg/m3]
# nppv = Net primary production of biomass expressed as carbon per unit volume in sea water [mg/m3/day]

# specify spatial limits (default below is Parker MacCready's boundary for the boundary of the LiveOcean model):
north = 53              # -90 to 90 degN          
south = 39              # -90 to 90 degN
west = -131             # -180 to 180 degE
east = -122             # -180 to 180 degE

# -  
# Specify the date_start and number_of_months from 11/2020 - present
date_start = '2022-01-01 00:00:00'      # ISO formatted string for the starting datetime for the data to be downloaded (starting day should be 01 and hh:mm:ss should be 00:00:00)
number_of_months = 12

# -  
# Specify the min and max depths to download (0 - 5728m)
dep_min = 0
dep_max = 5728


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
def get_extraction(data_request_options_dict):
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
# make monthly dt_list to extract from glorys
base = datetime.fromisoformat(date_start)
ndt = number_of_months
dt_list = []
dt_list = [base + relativedelta(months = x) for x in range(ndt)]

# prompt for the user name and password of the user account at https://data.marine.copernicus.eu/products
USERNAME = input('Enter your username: ')
PASSWORD = getpass.getpass('Enter your password: ')

# template dict that will be updated with new dates and output filenames during each iteration of the loop through days
data_request_options_dict_manual = {
    "service_id": "GLOBAL_ANALYSIS_FORECAST_BIO_001_028-TDS",
    "product_id": "global-analysis-forecast-bio-001-028-monthly",
    "date_min": " ",
    "date_max": " ",
    "longitude_min": float(west),
    "longitude_max": float(east),
    "latitude_min": float(south),
    "latitude_max": float(north),
    "depth_min": float(dep_min),
    "depth_max": float(dep_max),
    "variable": var_list,
    "motu": "https://nrt.cmems-du.eu/motu-web/Motu",
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
    out_fn = datetime.strftime(dt, 'glorys_biogeochem_%Y_%m') + '.nc'
    dstr_min = dt.strftime('%Y-%m-01 00:00:00')
    dd_str = str(calendar.monthrange(int(dt.strftime('%Y')), int(dt.strftime('%m')))[1])  # string of last day in this month
    dstr_max = dt.strftime('%Y-%m-'+dd_str+' 23:59:59')
    data_request_options_dict_manual["out_name"] = out_fn
    data_request_options_dict_manual["date_min"] = dstr_min
    data_request_options_dict_manual["date_max"] = dstr_max

    print(out_dir + out_fn)
    if os.path.isfile(out_fn):
        if force_overwrite:
            os.remove(out_fn)
    if not os.path.isfile(out_fn):
        result = get_extraction(data_request_options_dict_manual)
        f.write('\n ' + datetime.strftime(dt, '%Y_%m') + ' ' + result)
            
# - - -
# final message
totmin = (time.time() - tt1)/60             # total time elapsed for loop over all datetimes in minutes
print('')
print('All downloads are completed.')
print('Total time elapsed: %0.1f minutes' % totmin)
f.close()       # close log of successful downloads


