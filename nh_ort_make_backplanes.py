#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 23:42:14 2018

@author: throop
"""

import math      
import astropy
from   astropy.io import fits
import numpy as np
import spiceypy as sp
from   astropy.visualization import wcsaxes
import hbt
from   astropy.wcs import WCS
import os
import matplotlib.pyplot as plt
import glob

import random
import time
import sys
from multiprocessing import Process, Queue

from create_backplanes_fits import create_backplanes_fits
from plot_backplanes        import plot_backplanes

# def nh_ort_make_backplanes(frame = '2014_MU69_SUNFLOWER_ROT', digit_filter=None):
def nh_ort_make_backplanes(digit_filter, frame, q):
    
    """
    Process all of the MU69 ORT files. 
    
    Takes Simon's WCS'd FITS files as inputs, and creates backplaned FITS as output.
    
    Call this function in order to generate the backplanes from Simon's WCS files.

    Thus function is part of HBT's pipeline, and not a general-purpose routine.
    
    Arguments
    -----

    frame:
        The SPICE frame to use
    
    digit_filter:
        '12', '34', etc -- something to filter the FITS files by.
    q:
        The multiprocessor queue object.
    
    NB: I could not figure out how to pass keyword arguments  to the Process() function.
    So, that's why this function uses positional arguments only.           
    """

# =============================================================================
# Initialize
# =============================================================================

    do_print_diag = False

    do_plot    = True
    do_clobber = True
    
    name_target   = 'MU69'
    name_observer = 'New Horizons'
    # frame         = '2014_MU69_SUNFLOWER_ROT'  # Change this to tuna can if needed, I think??
    # frame         = '2014_MU69_TUNACAN_ROT'
    # frame         = '2014_MU69_ORT4_1'  # Change this to tuna can if needed, I think??
    
# =============================================================================
#     Get a proper list of all the input files
# =============================================================================
    
    do_ORT1 = False
    do_ORT3 = False
    do_ORT2 = False
    do_ORT4 = False
    do_ACTUAL = True  # Run this on actual OpNav data!
    
    do_force = True
    
#    dir_data_ort = '/Users/throop/Data/ORT1'
#    dir_in  = os.path.join(dir_data_ort, 'porter', 'pwcs_ort1')
#    dir_out = os.path.join(dir_data_ort, 'throop', 'backplaned')

    if do_ORT2:
        dir_data_ort = '/Users/throop/Data/ORT2'
        dir_in  = os.path.join(dir_data_ort, 'porter', 'pwcs_ort2')
        dir_out = os.path.join(dir_data_ort, 'throop', 'backplaned')
        files = glob.glob(os.path.join(dir_in, '*','*_ort2.fit'))

    if do_ORT3:    
        dir_data_ort = '/Users/throop/Data/ORT3'
        dir_in  = os.path.join(dir_data_ort, 'buie') # Using Buie backplanes, not Simon's.
        dir_out = os.path.join(dir_data_ort, 'throop', 'backplaned')
        files = glob.glob(os.path.join(dir_in, '*','*_ort3.fit'))
        frame         = '2014_MU69_TUNACAN_ROT'
        
    if do_ORT4:
        dir_data_ort = '/Users/throop/Data/ORT4'
        dir_in  = os.path.join(dir_data_ort, 'porter', 'pwcs_ort4')
        dir_out = os.path.join(dir_data_ort, 'throop', 'backplaned')
        files = glob.glob(os.path.join(dir_in, '*','*_pwcs.fits'))

    if do_ACTUAL:
        dir_data_ort = '/Users/throop/Data/MU69_Approach'
        dir_in  = os.path.join(dir_data_ort, 'porter')
        dir_out = os.path.join(dir_data_ort, 'throop', 'backplaned')

        # files = glob.glob(os.path.join(dir_in,'*', '*_pwcs.fits'))  # OpNav field data (older)        
        # files = glob.glob(os.path.join(dir_in, 'KALR_MU69_OpNav_L4_2018267', '*_pwcs2.fits')) # OpNav data
        # files = glob.glob(os.path.join(dir_in, 'KALR_MU69_OpNav_L4_2018284', '*_pwcs2.fits')) # OpNav data
        # files = glob.glob(os.path.join(dir_in, 'KALR_MU69_OpNav_L4_2018284', '*_pwcs2.fits')) # OpNav data
        # files = glob.glob(os.path.join(dir_in, 'KALR_MU69_OpNav_L4_2018284', '*_pwcs2.fits')) # OpNav data
        # files = glob.glob(os.path.join(dir_in, 'KALR_MU69_OpNav_L4_2018284', '*_pwcs2.fits')) # OpNav data
        # files = glob.glob(os.path.join(dir_in, 'KALR_MU69_OpNav_L4_2018287', '*_pwcs2.fits')) # OpNav data
        # files = glob.glob(os.path.join(dir_in, 'KALR_MU69_OpNav_L4_2018298', '*_pwcs2.fits')) # OpNav data
        # files = glob.glob(os.path.join(dir_in, 'KALR_MU69_OpNav_L4_2018301', '*_pwcs2.fits')) # OpNav data
        # files = glob.glob(os.path.join(dir_in, 'KALR_MU69_OpNav_L4_2018304', '*_pwcs2.fits')) # OpNav data
        # files = glob.glob(os.path.join(dir_in, 'KALR_MU69_OpNav_L4_2018311', '*_pwcs2.fits')) # OpNav data
        # files = glob.glob(os.path.join(dir_in, 'KALR_MU69_OpNav_L4_2018314', '*_pwcs2.fits')) # OpNav data
        # files = glob.glob(os.path.join(dir_in, 'KALR_MU69_OpNav_L4_2018315', '*_pwcs2.fits')) # OpNav data
        # files = glob.glob(os.path.join(dir_in, 'KALR_MU69_OpNav_L4_2018316', '*_pwcs2.fits')) # OpNav data
        # files = glob.glob(os.path.join(dir_in, 'KALR_MU69_OpNav_L4_2018317', '*_pwcs2.fits')) # OpNav data
        # files = glob.glob(os.path.join(dir_in, 'KALR_MU69_OpNav_L4_2018325', '*_pwcs2.fits')) # OpNav data
        # files = glob.glob(os.path.join(dir_in, 'KALR_MU69_OpNav_L4_2018326', '*_pwcs2.fits')) # OpNav data
        # files = glob.glob(os.path.join(dir_in, 'KALR_MU69_OpNav_L4_2018327', '*_pwcs2.fits')) # OpNav data
        # files = glob.glob(os.path.join(dir_in, 'KALR_MU69_OpNav_L4_2018328', '*_pwcs2.fits')) # OpNav data
        # files = glob.glob(os.path.join(dir_in, 'KALR_MU69_Hazard_L4_2018325', '*_pwcs2.fits')) # OpNav data

        files = glob.glob(os.path.join(dir_in, '*', '*_pwcs2.fits')) # OpNav data
        
        do_force = False
        do_clobber = False

# =============================================================================
# Check what FRAME we are using, and change output directory appropriately
# =============================================================================

    if 'TUNACAN' in frame.upper():
        dir_out = dir_out.replace('backplaned', 'backplaned_tunacan')
        
# =============================================================================
#     Filter files if needed
# =============================================================================
    
    # If desired, do a 'digit filter.' This filters the files down into a smaller number.
    # This is useful to do processing in parallel. Python global interpreter lock means
    # that only one CPU at a time can be used. To get around this, filter the files down,
    # and put each filter in its own Spyder tab.
    
    if digit_filter:
        
    # do_digit_filter = False

    # digit_filter = '12'
    # digit_filter = '34'
    # digit_filter = '56'
    # digit_filter = '78'
    # digit_filter = '90'
    
    # if (do_digit_filter):
        files_filtered = []
        for file in files:
            base = os.path.basename(file)
            digit = base[12]  # Match the penultimate digit in LORRI filename (e.g., lor_0405348852_pwcs ← matches '5')
                              # This is the digit that changes the most in the LORRI files, so it's a good choice.
            if (digit in digit_filter):
                files_filtered.append(file)
        if do_print_diag:
            print("Filtered on '{}': {} files → {}".format(digit_filter, len(files), len(files_filtered)))
        
        files = files_filtered            

# =============================================================================
# Start SPICE, if necessary
# =============================================================================
    
    if (sp.ktotal('ALL') == 0):
        sp.furnsh('kernels_kem_prime.tm')
        
# =============================================================================
# Loop and create each backplane
# =============================================================================
        
    count_run = 0
    count_skipped = 0
    
    
    for i,file_in in enumerate(files):
        if do_print_diag:
            print("{}/{}".format(i,len(files))) 
        file_out = file_in.replace(dir_in, dir_out)
        file_out = file_out.replace('_pwcs.fit', '_pwcs_backplaned.fit') # Works for both .fit and .fits
        file_out = file_out.replace('_pwcs2.fit', '_pwcs2_backplaned.fit') # Works for both .fit and .fits
    
        # Call the backplane function. Depending on settings, this will automatically run if a newer input file is 
        # received, and thus we need to regenerate the output backplane.
        
        try:
            create_backplanes_fits(file_in, 
                                      name_target,
                                      frame,
                                      name_observer,
                                      file_out,
                                      do_plot=False, 
                                      do_clobber=do_clobber,
                                      do_verbose=True)
            count_run += 1
            if (do_plot):
                plot_backplanes(file_out, name_observer = name_observer, name_target = name_target)
     
        except FileExistsError:
            if do_print_diag:
                print('File exists -- skipping. {}'.format(os.path.basename(file_out)))
            count_skipped +=1
            
    q.put(f'Digit filter {digit_filter}, {frame:25} {len(files)} files examined; ' +
          f'{count_run} run; {count_skipped} skipped')
       
# =============================================================================
# End of function
# =============================================================================

# =============================================================================
# Run the function if requested
# When run, this program regenerates all of the backplanes
# It uses multiprocessing to run these in parallel    
# =============================================================================

#%%%        
if (__name__ == '__main__'):
    
    file_tm = 'kernels_kem_prime.tm'
    sp.unload(file_tm)
    sp.furnsh(file_tm)

 # NB: This would be an ideal candidate for multi-processing 
 # NB: Done!
        
    # Set paramters here
    
    do_tuna      = False
    digit_filter = None
    
    # Run code here

    digit_filters = ['12', '34', '56', '78', '90']
    frames        = ['2014_MU69_SUNFLOWER_ROT']  #, '2014_MU69_TUNACAN_ROT']
    
    q = Queue()  # Start up the process queue

    func = nh_ort_make_backplanes
    
    procs   = []   # List of processes
    results = []   # List of results. This is empty, since we don't return anything
    
    # Loop over and start up all the child processes.
    # Wait between each spawn. Otherwise SP.FURNSH() seems to get confused
    
    for digit_filter in digit_filters:
        for frame in frames:
            proc = Process(target=func, args=(digit_filter, frame, q)) # Can't figure out how to pass keyword args here.
            proc.start()
            procs.append(proc)
            time.sleep(0.5)   # Sleep briefly.
            print(f'Started process with filter={digit_filter}, frame={frame}')
    
    for proc in procs:        
        
        results.append(q.get(True))  # No output to wait for -- so don't. We really should take output, though.
        
        proc.join()  # 'Wait until child process terminates'
     
    for result in results:
        print(result)

     

        
        