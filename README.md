# Vatican Observatory Summer School [[VOSS2023](https://www.vaticanobservatory.va/en/education/voss/voss-2023)]

# Project : Search for bright high-z QSOs in the SkyMapper/PAN-STARRS survey.

Proposed by: [*Giorgio Calderone*](mailto:giorgio.calderone@inaf.it) (INAF-Osservatorio Astronomico di Trieste, Italy)

## Purpose

The students will search for new, bright QSOs at z>2 in the SkyMapper/PAN-STARRS photometric survey, following a multi-disciplinary approach.

## Reference paper

- [Calderone et al. 2019](https://ui.adsabs.harvard.edu/abs/2019ApJ...887..268C/abstract): Finding the Brightest Cosmic Beacons in the Southern Hemisphere;

## Input catalogs

- PanSTARRS1 DR2 ([docs](https://outerspace.stsci.edu/display/PANSTARRS/PS1+StackObjectView+table+fields));

- Gaia DR3 ([docs](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html));

- AllWise ([docs](https://wise2.ipac.caltech.edu/docs/release/allwise/expsup/sec2_1a.html));

- Spectroscopic classification and redshifts ([fits](http://140.105.76.151:8000/VOSS_classifications.fits.gz))
  
  *(This is a collection of data from many smaller catalogs, prepared in advance to avoid dedicating time to minor issues).*
  
  Content of the file is as follows:
  
  - `qid`: primary key;
  
  - `RAd`, `DECd`: J2000 coordinates in degrees;
  
  - `objtype`: spectroscopic classification;
  
  - `z_spec`: spectroscopic redshift.

## Tasks

- Data collection: download data from SkyMapper/PAN-STARRS and auxiliary databases (e.g. Gaia, WISE, QSO catalogs);
  
  - See section "Input Catalogs";

- Data preparation: cross-match the input catalogs, preliminary source classification and feature selection;
  
  - Identify matching entries in all input catalogs by cross-matching coordinates;
    - Mark duplicated entries;
    - Generate a single table with one source per line and all relevant columns from the input catalogs;
  - Identfy stars in the input catalogs using only available information;
  - Identify the relevant features to be used for training.  Is caling relevant?;
  
  Suggestion: do not underestimate issues related to data size! (RAM, processing time, disk space...).

- QSO candidate selection train a machine learning model to (1) predict a source classification and (2) estimate its redshift (if the source is extragalactic):
  
  - Prepare a code to split the main table into three datasets:
    
    - Training set;
    - Test set;
    - Unclassified set;
    
    Notes: use stratified approach, shuffle data;
  
  - Prepare code to estimate the relevant metrics (classification: precision, TPR, f1-score; regression: rmse, MAD, fraction of outliers) and print confusion matrices;
  
  - Identify suitable ML algorithm(s) to classify source and estimate redshifts (methods may be different for classification and regression);
    
    - Lay down a strategy to tune the hyper-parameters;

- Estimate the performances of the selection process and propose possible improvements:
  
  - Train model(s), estimate performances on test set, repeat to estimate average performances;
  - How to deal with imbalanced training dataset?
  - How to improve redshift estimates?  How to reduce outliers?
  - How to prioritize observations to maximize success rate?
  - How to estimate classification probabilities?  Is [probability calibration](https://scikit-learn.org/stable/modules/calibration.html) relevant to prioritize observations?
  - Can we estimate feature importance? What can we learn from it?
