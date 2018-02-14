#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 15:38:48 2018

@author: throop
"""

import pdb
import glob
import math       # We use this to get pi. Documentation says math is 'always available' 
                  # but apparently it still must be imported.
from   subprocess import call
import warnings
import pdb
import os.path
import os
import subprocess

import astropy
from   astropy.io import fits
from   astropy.table import Table
import astropy.table   # I need the unique() function here. Why is in in table and not Table??
import matplotlib
import matplotlib.pyplot as plt # pyplot
from   matplotlib.figure import Figure
import numpy as np
import astropy.modeling
from   scipy.optimize import curve_fit
#from   pylab import *  # So I can change plot size.
                       # Pylab defines the 'plot' command
import spiceypy as sp
#from   itertools import izip    # To loop over groups in a table -- see astropy tables docs
from   astropy.wcs import WCS
from   astropy.vo.client import conesearch # Virtual Observatory, ie star catalogs
from   astropy import units as u           # Units library
from   astropy.coordinates import SkyCoord # To define coordinates to use in star search
#from   photutils import datasets
from   scipy.stats import mode
from   scipy.stats import linregress
from   astropy.visualization import wcsaxes
import time
from   scipy.interpolate import griddata
from   importlib import reload            # So I can do reload(module)
import imreg_dft as ird                    # Image translation
import struct

import re # Regexp
import pickle # For load/save

from   datetime import datetime

import scipy

from   matplotlib.figure import Figure

# HBT imports

import hbt

class ort_track3:  # Q: Is this required to be same name as the file?

# =============================================================================
# Initialize the method.
# Read the specified track3 file into memory, from disk
# =============================================================================
    
    def __init__(self, name, dir_base='/Users/throop/data/ORT1/kaufmann/deliveries', binfmt = 2):
        
        """
        Initialize the method.
        
        Paramateters
        ------
            
        name:
            The name of the run. This is a slash-separated string, such as 
            `'ort1-0001/1000010/speed1/beta_2.6e-04/subset00'`
             
        dir_base:
            The top-level directory that I download files from ixion into. Typically this ends in `deliveries`.
        """    
            
        self.name = name
    
        parts = name.split('/')

        dir = name
        
        file_header =(parts[0].replace('-', '_') + '_' + parts[1] + '_' + 
                      parts[2].replace('1', '0').replace('2', '1') + '_' +
                      parts[3] + '_' + parts[4] +
                      '.header')

        file_data = f'model.array{binfmt}'
        
        file_header_full = os.path.join(dir_base, dir, file_header)
        file_data_full   = os.path.join(dir_base, dir, file_data)

        # Read the datafiles. Using code fragment from DK email 13-Feb-2018

        # Read header file
        
        f = open(file_header_full, 'r')
        text = f.read()
        f.close()
        lines = text.split('\n')
        nx = int(lines[0].split()[0])
        ny = int(lines[1].split()[0])
        nz = int(lines[2].split()[0])
        km_per_cell_x = float(lines[3].split()[0])
        km_per_cell_y = float(lines[4].split()[0])
        km_per_cell_z = float(lines[5].split()[0])
        
        # Read and process binary file
        
        density = np.zeros((nx, ny, nz), np.float32)
        f = open(file_data_full, 'rb')
        data = f.read()
        f.close()
                
        if binfmt == 1:
            for i in range(nx):
                for j in range(ny):
                    for k in range(nz):
                        start = 4*(i*ny*nz + j*nz + k)
                        (density[k,j,i],) = struct.unpack('f', data[start:start+4])
        else: # binfmt == 2
            statinfo = os.stat(file_data_full)
            nentries = int(statinfo.st_size / 10) # record size = 10 bytes (3 2-byte ints + 4-byte float)
                                                  # int / int = float, in Python -- not sure why
                   
            for i in range(nentries):
                start = 10*i
                (ix,iy,iz) = struct.unpack('hhh', data[start:start+6])
                (density[iz-1,iy-1,ix-1],) = struct.unpack('f', data[start+6:start+10])
    
        self.density = density
        self.km_per_cell_x = km_per_cell_x
        self.km_per_cell_y = km_per_cell_y
        self.km_per_cell_z = km_per_cell_z
        
        # We should read the full header in to the class as well. But this will require more parsing.
        
        return

# =============================================================================
# Plot the distributions
# =============================================================================
    
    def plot(self):
        
        stretch_percent = 90    
        stretch = astropy.visualization.PercentileInterval(stretch_percent) # PI(90) scales to 5th..95th %ile.
 
        (nx, ny, nz) = np.shape(self.density)
        xpos = hbt.frange(-nx/2, nx/2)*self.km_per_cell_x
        ypos = hbt.frange(-ny/2, ny/2)*self.km_per_cell_y
        zpos = hbt.frange(-nz/2, nz/2)*self.km_per_cell_z

        extent = (ypos[0], ypos[-1], zpos[0], zpos[-1])
        
        for axis in (0,1,2):
            plt.subplot(2,2,axis+1)
            plt.imshow(stretch(np.sum(self.density, axis=axis)), extent=extent)
            plt.ylabel('Pos [km]')
            plt.xlabel('Pos [km]')
            if (axis == 2):
                plt.colorbar()
            plt.title(self.name)
        
        plt.show()
        
        return

# =============================================================================
# Run the file
# =============================================================================
    
if __name__ == '__main__':
    
    dir_base='/Users/throop/data/ORT1/kaufmann/deliveries'
    
    runs_full = glob.glob(os.path.join(dir_base, '*', '*', '*', '*', '*'))

    for run_full in runs_full:
        run = run_full.replace(dir_base, '')[1:]
        ring = ort_track3(run)
        ring.plot()
    
     