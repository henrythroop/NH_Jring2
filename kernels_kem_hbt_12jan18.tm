This is NHGV's default kernel set for the NH MU69 Prime trajectory flyby. It
includes all SPICE files used by NHGV, including frames kernels, trajectories
for s/c and many planets and satellites, MU69, frames kernels, instrument
kernels, etc.

All of these files exist on ixion, and can be used by making a symlink from 
GV's kernel directory into a local directory:

   ln -s /home/html/nh/gv-dev/kernels .

After doing so, the entire kernel set can be used by passing FURNSH() the name
of *this file*.

HBT 12-Jan-2017

\begindata
KERNELS_TO_LOAD = (
'kernels/pck00009.tpc',
'kernels/p4p5.revised.bsp',
'kernels/plu020.bsp',
'kernels/de413.bsp',
'kernels/mar063.bsp',
'kernels/jup204.bsp',
'kernels/jup260.bsp',
'kernels/sat077_2000-2025.bsp'
'kernels/sat227.bsp',
'kernels/ura027-3.bsp',
'kernels/nep016.bsp',
'kernels/nh_plu017.bsp',
'kernels/2014MU69_SBP_170528_may25a.bsp',
'kernels/nh_v220.tf',
'kernels/nh_ralph_v100.ti',
'kernels/nh_lorri_v100.ti',
'kernels/nh_swap_v200.ti',
'kernels/nh_sdc_v100.ti',
'kernels/nh_pepssi_v110.ti',
'kernels/nh_alice_v200.ti',
'kernels/nh_alice_rows.ti',
'kernels/nh_alice_rows.tf',
'kernels/nh_rex_v100.ti',
'kernels/nh_fss_v000.ti',
'kernels/nh_astr_v000.ti',
'kernels/naif0012.tls',
'kernels/new-horizons_1535.tsc',
'kernels/gv_pck.tpc',
'kernels/gv_naif_ids.txt',
'kernels/pluto_solar_heliographic.tf',
'kernels/gv_pluto_smallsats.tf',
'kernels/gv_smallbodies.tf',
'kernels/plu013.bsp',
'kernels/Nix_ephem_v02.bsp',
'kernels/Hydra_ephem_v02.bsp'
'kernels/nh_nom_20060119_20150727_v03.bsp',
'kernels/nh_pred_20141201_20190301_od122.bsp',
'kernels/nh_ref_20150801_20190901_od128_tcm22.bsp'
'kernels/merged_nhpc_2007_v001.bc',
'kernels/NavSE_plu047_od122.bsp',
'kernels/NavPE_de433_od122.bsp',
'kernels/nh_scispi_2015_pred.bc',
'kernels/nh_scispi_2015_recon.bc',
'kernels/nh_lorri_wcs.bc'
'kernels/merged_18359_v1_cmd.bc'
'kernels/NavPE_de433_od128.bsp',
'kernels/2014MU69_SBP_170825_noocc5.bsp',
'kernels/nh_nom_20170201_20210714_v13_prime.bsp',
'kernels/gv_pluto_smallsats_lhr.tf',
'kernels/gv_pck.tpc',
'kernels/mu69_sunflower.tf',
)
