from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import os, sys
from astropy.table import Table
from astropy.io import fits
from os import listdir
import pandas as pd
from astropy import units as u
from astropy.table import Table

from astroML.crossmatch import crossmatch_angular
from tqdm import tqdm



main_path = sys.path[0].replace('/code','')
os.chdir(main_path)


alldata = Table.read(main_path+'/data/final_cat.fits')
alldata = alldata.to_pandas()
objtype_list = list()
alldata.objtype = alldata.objtype.str.decode("utf-8")
alldata.objtype[np.abs(alldata.parallax_over_error) > 3*np.std(alldata.parallax_over_error)] = 'Star'
alldata.objtype[np.abs(alldata.pm/alldata.pmra_error) > 3*np.std(alldata.pm/alldata.pmra_error)] = 'Star'
alldata.objtype[np.abs(alldata.pm/alldata.pmdec_error) > 3*np.std(alldata.pm/alldata.pmdec_error)] = 'Star'

features = ['w1pro','w2pro','w3pro','Q1_SkyM11_mag_u','Q1_SkyM11_mag_v',  
            'Q1_SkyM11_mag_g', 'Q1_SkyM11_mag_r', 'Q1_SkyM11_mag_i']

label = ['objtype']

