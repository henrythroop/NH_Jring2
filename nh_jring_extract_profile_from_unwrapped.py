#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 12:45:37 2017

Extracts radial *or* azimuthal profile from unwrapped ring images.
This is a more flexible routine than the one that extracts *both* profiles

  nh_jring_extract_profile_from unwrapped:  This routine,  more flexible. One profile at a time.
  nh_jring_extract_profiles_from unwrapped: Other routine, less flexible. Two profiles at a time.

bins_radius:  Input: the definition of radius  bins in the unwrapped image (required)
bins_azimuth: Input: The definition of azimuth bins in the unwrapped image (required)

range_profile [if azimuthal]:  Portion of radius  range to use, when extracting azimuthal profile
                       Can be a scalar fraction (0.5), or vector fraction (0.3, 0.6), or vector distance (128000,129000)
   
range_profile [if radial]:     Portion of azimuth range to use, when extracting radial    profile.
                       Can be a scalar fraction (0.5) only.

type_profile:        String, 'radial' or 'azimuthal' (case-insensitive, first letter checked only)

mask_unwrapped: A boolean mask, indicating whether to use individual pixels in the final output, or not.

@author: throop
"""

def nh_jring_extract_profile_from_unwrapped(im_unwrapped, bins_radius, bins_azimuth,
                                            range_profile, type_profile,
                                            mask_unwrapped=False):

    import hbt
    import numpy as np
    from   scipy.interpolate import griddata
    import warnings

    if type(mask_unwrapped) == type(np.array([])):
        DO_MASK = True

    if (DO_MASK):    
        is_good_unwrapped = (mask_unwrapped == False)

        im_unwrapped_masked = im_unwrapped.copy()
        im_unwrapped_masked[is_good_unwrapped == False] = np.nan
    
        im2 = im_unwrapped_masked

    else:
        im2 = im_unwrapped

# Extract the radial profile, if requested

    if (type_profile.upper()[0] == 'RADIAL'[0]):
        
# Extract the radial profile, if requested.

#  We use a subset of the azimuth angles.
#    e.g., if range=0.1, then extract the central 10% of the azimuth angles
    
        bin_0 = int(hbt.sizex(bins_azimuth) * (0.5 - (0.5 * range_profile)))  
        bin_1 = int(hbt.sizex(bins_azimuth) * (0.5 + (0.5 * range_profile)))

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)    
            profile_radius  = np.nanmean(im2[:, bin_0:bin_1],1)
        return(profile_radius)
        
# Extract the azimuthal profile, if requested
   
    if (type_profile.upper()[0] == 'AZIMUTHAL'[0]):
   
      if (isinstance(range_profile, float)):   # If passed a single radial range value, like 0.5, then use as fraction
          bin_0 = int(hbt.sizex(bins_radius) * (0.5 - (0.5 * range_profile)))
          bin_1 = int(hbt.sizex(bins_radius) * (0.5 + (0.5 * range_profile)))

                                        # If passed two radial range values, like (0.3, 0.4), then use as fractions
      elif ( isinstance(range_profile, tuple) and (range_profile[0] < 1) and (range_profile[1] < 1) ):
          bin_0 = int(hbt.sizex(bins_radius) * (range_profile[0]))
          bin_1 = int(hbt.sizex(bins_radius) * (range_profile[1]))
    
                                        # If passed two radial range values, like (128000,129000), then use as dist's.
      elif ( isinstance(range_profile, tuple) and (range_profile[0] > 1) and (range_profile[1] > 1) ):
          bin_0 = hbt.x2bin(range_profile[0], bins_radius)
          bin_1 = hbt.x2bin(range_profile[1], bins_radius)

      else:
          raise(ValueError("Cannot parse range!"))
          
      with warnings.catch_warnings():
         warnings.simplefilter("ignore", category=RuntimeWarning)    
         profile_azimuth = np.nanmean(im2[bin_0:bin_1, :],0)
         
      return(profile_azimuth)