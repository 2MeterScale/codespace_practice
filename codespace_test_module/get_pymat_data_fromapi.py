#!/usr/bin/env python

# %%
import os
import pickle
from chempy import Substance
from mp_api.client import MPRester

MY_API_KEY = "09vnTU6R8jWfPhuZ6bFs3niTwe1F03x4"

# %%
# Output directory
path_output_dir = "/workspaces/codespace_practice/train_material_list/"
if not os.path.exists(path_output_dir):
    os.makedirs(path_output_dir)
    
# %%
#読み取り予定のリストを取得
with open("/workspaces/codespace_practice/codespace_test_module/formula_list_from_matproj.pkl", "rb") as f:
    formula_list = pickle.load(f)

# %%
# define physical properties/infos you want to obtain
properties = ["material_id", "formula_pretty", "band_gap", "efermi", "energy_above_hull"]
name = formula_list[1:]
with MPRester(MY_API_KEY) as mpr:
    results = mpr.materials.summary.search(formula=name, fields=properties)


#%%
print(results[0])
# %%
for mat in results:
    ofile = path_output_dir + mat.material_id + "_" + mat.formula_pretty + ".pickle"
    # mat.structure.to(filename = ofile)
    # 原因は不明だが.structureで取り出すことが出来ない
    # 辞書式にしてpickleで保存する

    output = {"formula": mat.formula_pretty, "material_id": mat.material_id, "band_gap": mat.band_gap, "efermi": mat.efermi, "energy_above_hull": mat.energy_above_hull}
    if os.path.exists(ofile):
        print(f"Warning: The file {ofile} exists and will be overwritten.")
    try:
        with open(ofile, "wb") as f:
            pickle.dump(output, f)
    except Exception as e:
        print("Dumpling failed: ", str(e))
        

# %%
