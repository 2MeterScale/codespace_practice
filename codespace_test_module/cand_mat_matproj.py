#materials projectからNNに突っ込んで予測するための
#情報を取得するためのソースコード
#ひとまずホウ化物？とかになるのかなという感じ
#例えばホウ化物で構成元素が3つ以上とか

# %%
import os
import pickle
import pandas as pd
from chempy import Substance
import periodictable
import ast

pd.options.display.max_columns = 100
pd.options.display.max_rows = 100

from mp_api.client import MPRester

MY_API_KEY = "09vnTU6R8jWfPhuZ6bFs3niTwe1F03x4"

# %%
# Output directory
path_output_dir = "/workspaces/codespace_practice/candidate_material_list/"
if not os.path.exists(path_output_dir):
    os.makedirs(path_output_dir)



# %%
# define physical properties/infos you want to obtain
properties = ["material_id", "formula_pretty", "band_gap", "efermi", "energy_above_hull"]
#nameは*の数で構成する元素数を指定できる？
name = "**"
#nelements_maxで構成する元素数の最大値を指定できる
#nelements_max = 5
with MPRester(MY_API_KEY) as mpr:
    results = mpr.materials.summary.search(fields=properties, elements = ["B"])


# %%
#この得たデータをpickleで保存する理由が!ありません!
#地産地消でcsvにしよう!
cand_df = pd.DataFrame(columns = ["formula", "material_id", "band_gap", "efermi", "energy_above_hull"])
for mat in results:
    subdata = {
        "formula": mat.formula_pretty, 
        "material_id": mat.material_id, 
        "band_gap": mat.band_gap, 
        "efermi": mat.efermi, 
        "energy_above_hull": mat.energy_above_hull
    }
    
    subdf = pd.DataFrame(subdata, index=[0])
    
    cand_df = pd.concat([cand_df, subdf], axis=0)



# %%
cand_df = cand_df.reset_index(drop = True)
cand_df["comp_atoms"] = cand_df["formula"].apply(lambda x: Substance.from_formula(x).composition)
cand_df["sorted_keys_comp_atoms"] = cand_df["formula"].apply(lambda x: sorted(Substance.from_formula(x).composition.keys()))
cand_df["comp_number"] = cand_df.apply(lambda row: ''.join(f'{k}{row["comp_atoms"][k]}' for k in row["sorted_keys_comp_atoms"]), axis=1)

chosen_material_list = []

for i, subdf in cand_df.groupby("comp_number"):
    if len(subdf) > 1:
        subdf = subdf.sort_values("energy_above_hull")
        chosen_material_list.append(subdf.index[0])
        
    else:
        chosen_material_list.append(subdf.index[0])

chosen_cand_df = cand_df.loc[chosen_material_list]



# %%
#できたものは保存しましょうね～
chosen_cand_df.to_csv("/workspaces/codespace_practice/candidate_material_list/candidate_material_list.csv", index=False)


# %%
chosen_cand_df = pd.read_csv("/workspaces/codespace_practice/candidate_material_list/candidate_material_list.csv")
chosen_cand_df["comp_atoms"] = chosen_cand_df["comp_atoms"].apply(ast.literal_eval)


# %%
chosen_cand_df["new_formula"] = None

try:
    for i in range(len(chosen_cand_df)):
        dict_keys = list(chosen_cand_df.loc[i, "comp_atoms"].keys())

        comp = ""
        
        for j in range(len(dict_keys)):
            element = str(periodictable.elements[dict_keys[j]])
            comp += element + str(chosen_cand_df.loc[i, "comp_atoms"][dict_keys[j]])
            
        chosen_cand_df.loc[i, "new_formula"] = comp
        
except Exception as e:
    print(e)
    print("Error: ", i, j)



# %%
display(chosen_cand_df)
# %%
