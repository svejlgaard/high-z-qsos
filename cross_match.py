from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import os, sys
from astropy.table import Table
from astropy.io import fits
from os import listdir
import pandas as pd
from astropy import units as u
from astroML.crossmatch import crossmatch_angular
from tqdm import tqdm



main_path = sys.path[0].replace('/code','')
os.chdir(main_path)


def init_load(data_path): 
    samples = Table.read(data_path)
    lens = [len(samples[name]) for name in samples.colnames]
    lens = np.unique(lens)[0]
    dataframe = pd.DataFrame()
    with fits.open(data_path) as data:
        columns=(data[1].columns)
        for c in columns:
            if data[1].data[c.name].shape==(lens, 1):
                datacol=data[1].data[c.name][:,0]
            else:
                datacol=data[1].data[c.name]
            dataframe[c.name]=datacol
            if datacol.dtype.kind=='U': 
                print("removed ",c.name)
                continue
            elif datacol.dtype.kind=='U': dataframe[c.name]=np.asarray(datacol)
            else:dataframe[c.name]=np.asarray(datacol).byteswap().newbyteorder('<')
    return dataframe



voss_path = '/data/VOSS_classifications.fits'
vossdata = init_load(main_path+voss_path)
vossdata['objtype'] = vossdata['objtype'].astype(str)
vosscoord = vossdata[['RAd','DECd']].to_numpy()

#gaia_path = '/data/subset_Gaia_EDR3.fits'
#panstarrs_path = '/data/subset_PanSTARRS1DR2.fits'
#wise_path = '/data/subset_AllWise.JBb_uiex.fits'
wise_path = '/data/AllWise.fits'
panstarrs_path = '/data/PanSTARRS1DR2.fits'
gaia_path = '/data/Gaia_EDR3.fits'


gaia_cols = ['ra','dec']
panstarrs_cols = ['raStack','decStack']

cat_cols = [gaia_cols,panstarrs_cols,gaia_cols]

catalogs = ['gaia','panstarrs','wise']
cat_paths = [gaia_path,panstarrs_path,wise_path]

tau = 0.95

def flags(dist, ind):
    no_match = np.zeros_like(dist)
    not_single_match = np.zeros_like(dist)
    miss = np.isinf(dist)
    no_match[miss] = 1
    unique, doubles = np.unique(ind[~miss], return_counts=True)
    double_val = unique[doubles > 1]
    print(double_val)
    for d in double_val:
        double_ind = np.where(ind == d)[0]
        not_single_match[double_ind] = 1
    final_match = no_match + not_single_match
    return final_match


for c,cat in enumerate(catalogs):

    catdata = init_load(main_path+cat_paths[c])
    print(catdata.keys().to_list())


    catcoord = catdata[cat_cols[c]].to_numpy()
    

    max_radius = 1. / 3600  # 1 arcsec
    dist_cat_to_voss, ind_cat_to_voss = crossmatch_angular(catcoord, vosscoord, max_radius)
    inv_flag_match = flags(dist_cat_to_voss, ind_cat_to_voss)

    dist_voss_to_cat, ind_voss_to_cat = crossmatch_angular(vosscoord, catcoord, max_radius)
    flag_match = flags(dist_voss_to_cat, ind_voss_to_cat)
    matches = np.zeros_like(vosscoord[:,0])
    matches[:] = np.nan
    for i,ind in enumerate(ind_voss_to_cat):
        if not np.isinf(dist_voss_to_cat[i]):
            matches[i] = catdata['_id'][ind]
            flag_match[i] += inv_flag_match[ind]
    
    vossdata[cat+'_match'] = matches
    vossdata[cat+'_double'] = flag_match

    
    print(len(flag_match[flag_match ==0]))
     

    match = ~np.isinf(dist_voss_to_cat)

    dist_match = dist_voss_to_cat[match]
    dist_match *= 3600



    fig, ax = plt.subplots(figsize=(11,9))
    ax.hist(dist_match, histtype='stepfilled', ec='k', fc='#AAAAAA',bins=100,density=True)
    ax.set_xlabel('radius of match (arcsec)')
    ax.set_ylabel('N(r, r+dr)')
    ax.text(0.95, 0.95,
            "Total objects: %i\nNumber with match: %i" % (vosscoord.shape[0],
                                                        np.sum(match)),
            ha='right', va='top', transform=ax.transAxes)
    ax.set(title=cat)

    plt.savefig(main_path+f'/figures/{cat}_dist.pdf')


vossdata = vossdata[(vossdata['gaia_double'] == 0) & (vossdata['wise_double'] == 0) & (vossdata['panstarrs'] == 0)]
print(vossdata)