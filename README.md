# get_glorys
Download of GLORYS model outputs using Python

# ----------
# get_glorys_reanalysis_daily.py 
# 
# Python script to extract daily GLORYS model output
# from the Global Ocean Physics Reanalysis between 1/1/1993 to 12/31/2020
#
# This script is used to download from:

# https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/download?dataset=cmems_mod_glo_phy_my_0.083_P1D-m

# by Greg Pelletier (gjpelletier@gmail.com) for standalone use (https://github.com/gjpelletier/get_glorys)
# ----------

INSTRUCTIONS

Before using this script, it is first necessary to establish a free account with https://data.marine.copernicus.eu/
Your username will be assigned when you establish your account. Your password should not include special characters.

After you have established an account, the following are the instructions for using this script:

1) Edit the user input section below as needed, specify the following:
 		- list of variables to be extracted from any combination, e.g. var_list = ["so","thetao","uo","vo","zos"]
 		- west, east, south, and north extent of the bounding box to be extracted
  		- the name of the OUTPUT_DIRECTORY where the glorys data will be saved as output
 		- the date_start and number_of_days of the period to be extracted (between 1/1/1993 and 12/31/2020)
2) Run this script in python or ipython
3) Enter your username and password when prompted
4) During execution you sould see the progress of each daily file that is extracted during the period of interest 
   from beginning to end. Each nc file name has the format glorys_yyyy_MM_dd.nc to indicate the date stamp

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
