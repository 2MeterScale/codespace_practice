#!/usr/bin/env python
from mp_api.client import MPRester
import os

MY_API_KEY="09vnTU6R8jWfPhuZ6bFs3niTwe1F03x4"

#with MPRester( MY_API_KEY ) as mpr:
#  list_of_available_fields = mpr.materials.summary.available_fields
#print(list_of_available_fields)
#
#['builder_meta', 'nsites', 'elements', 'nelements', 'composition', 'composition_reduced', 'formula_pretty', 'formula_anonymous', 'chemsys', 'volume', 'density', 'density_atomic', 'symmetry', 'property_name', 'material_id', 'deprecated', 'deprecation_reasons', 'last_updated', 'origins', 'warnings', 'structure', 'task_ids', 'uncorrected_energy_per_atom', 'energy_per_atom', 'formation_energy_per_atom', 'energy_above_hull', 'is_stable', 'equilibrium_reaction_energy_per_atom', 'decomposes_to', 'xas', 'grain_boundaries', 'band_gap', 'cbm', 'vbm', 'efermi', 'is_gap_direct', 'is_metal', 'es_source_calc_id', 'bandstructure', 'dos', 'dos_energy_up', 'dos_energy_down', 'is_magnetic', 'ordering', 'total_magnetization', 'total_magnetization_normalized_vol', 'total_magnetization_normalized_formula_units', 'num_magnetic_sites', 'num_unique_magnetic_sites', 'types_of_magnetic_species', 'bulk_modulus', 'shear_modulus', 'universal_anisotropy', 'homogeneous_poisson', 'e_total', 'e_ionic', 'e_electronic', 'n', 'e_ij_max', 'weighted_surface_energy_EV_PER_ANG2', 'weighted_surface_energy', 'weighted_work_function', 'surface_anisotropy', 'shape_factor', 'has_reconstructed', 'possible_species', 'has_props', 'theoretical', 'database_IDs']

# See https://api.materialsproject.org/redoc
# or  https://api.materialsproject.org/docs#/Materials%20Summary/search_materials_summary__get
# or  https://docs.materialsproject.org/downloading-data/using-the-api


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

# define physical properties/infos you want to obtain
properties = ['formula_pretty','material_id','structure','symmetry','is_metal','band_gap']
name = "**O3"
with MPRester( MY_API_KEY ) as mpr:
    results = mpr.materials.summary.search(formula=name, band_gap=(band_gap_min, band_gap_max), spacegroup_symbol = sg_symb, is_stable=_is_stable, is_metal=_is_metal, fields=properties)


#Output
path_output_dir = "./ABO3_cif/"
if not os.path.exists(path_output_dir):
    os.makedirs(path_output_dir)
for mat in results:
    #print(mat.material_id, mat.formula_pretty)
    #print(mat.symmetry.symbol)
    #print(mat.is_metal, mat.band_gap)
    ofile = path_output_dir+mat.material_id+"_"+mat.formula_pretty+".cif"
    mat.structure.to(filename = ofile)

#Get physical properties of SrBO3 systems (B="V", "Ti", or "Co")
# define physical properties/infos you want to obtain
properties = ['formula_pretty', "band_gap", "formation_energy_per_atom", "symmetry"]
name = "**O3"
with MPRester( MY_API_KEY ) as m:
    for atm in ["V","Ti","Co"]:
        results = mpr.materials.summary.search(formula=name, elements=[atm, "Sr"], fields=properties)

        #Output
        for mat in results:
            print(mat.formula_pretty)
            print("  band_gap:", mat.band_gap)
            print("  formation_energy_per_atom:", mat.formation_energy_per_atom)
            print("  symmetry:", mat.symmetry)