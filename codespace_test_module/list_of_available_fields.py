#!/usr/bin/env python
from mp_api.client import MPRester

MY_API_KEY="09vnTU6R8jWfPhuZ6bFs3niTwe1F03x4"


#Get physical properties of SrBO3 systems (B="V", "Ti", or "Co")
# define physical properties/infos you want to obtain
properties = ['formula_pretty', "band_gap", "efermi"]
name = "La2CuO4"
with MPRester( MY_API_KEY ) as mpr:
    results = mpr.materials.summary.search(formula=name, fields=properties)

    #Output
    for mat in results:
        print(mat.formula_pretty)
        print("  band_gap:", mat.band_gap)
        print("  efermi:", mat.efermi)