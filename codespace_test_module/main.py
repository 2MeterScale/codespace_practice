#!/usr/bin/env python
from mp_api.client import MPRester
import os

MY_API_KEY="09vnTU6R8jWfPhuZ6bFs3niTwe1F03x4"

#Get cif files of ABO3 systems
# Only for stable insulators with band_gap < 1 and spacegroup = Pm-3m
band_gap_min = None
band_gap_max = 1.0 
sg_symb = "Pm-3m"
_is_stable=True
_is_metal=False
# Only for stable metals (band_gap = 0) with spacegroup = Pm-3m
#band_gap_min = None
#band_gap_max = None
#sg_symb = "Pm-3m"
#_is_stable=True
#_is_metal=True

#Get physical properties of SrBO3 systems (B="V", "Ti", or "Co")
# define physical properties/infos you want to obtain
properties = ['formula_pretty', "band_gap", "formation_energy_per_atom", "symmetry", "efermi"]
name = "NaAlH4"
with MPRester( MY_API_KEY ) as mpr:
    results = mpr.materials.summary.search(formula=name, fields=properties)

    for mat in results:
        print(mat.formula_pretty)
        print("  band_gap:", mat.band_gap)
        print("  formation_energy_per_atom:", mat.formation_energy_per_atom)
        print("  symmetry:", mat.symmetry)
        print("  efermi:", mat.efermi)