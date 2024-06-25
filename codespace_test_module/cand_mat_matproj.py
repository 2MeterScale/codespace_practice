# materials projectからNNに突っ込んで予測するための
# 情報を取得するためのソースコード
# ひとまずホウ化物？とかになるのかなという感じ
# 例えばホウ化物で構成元素が3つ以上とか

# %%
import os

import pandas as pd
import periodictable
from chempy import Substance
from mp_api.client import MPRester
# import ast

pd.options.display.max_columns = 100
pd.options.display.max_rows = 100

MY_API_KEY = "09vnTU6R8jWfPhuZ6bFs3niTwe1F03x4"

# %%
# Output directory
path_output_dir = "/workspaces/codespace_practice/candidate_material_list/"
if not os.path.exists(path_output_dir):
    os.makedirs(path_output_dir)


# %%
# define physical properties/infos you want to obtain
properties = ["material_id", "formula_pretty", "band_gap", "efermi", "energy_above_hull"]
# nameは*の数で構成する元素数を指定できる？
name = "**"
_is_stable = True

# 他にはBa, Sr, Niとか?
# 上原先生の助言の元,C,Al,Si,Li,B,Niで半導体周りでやってみる
# 酸素を除外したデータでもやってみる
# 酸素除外について、あまり意味がないというのと
# 窒化物を研究室で作ることが出来ないのでこれを除外する

element_filter = ["C", "Al", "Si", "Li", "B", "Ni"]


with MPRester(MY_API_KEY) as mpr:
    for atm in element_filter:
        results = mpr.materials.summary.search(fields=properties, elements=[atm], exclude_elements=["Ba", "Cu", "Y", "Fe", "Hg", "N"], is_stable=_is_stable)

        cand_df = pd.DataFrame(columns=["formula", "material_id", "band_gap", "efermi", "energy_above_hull"])

        for mat in results:
            subdata = {"formula": mat.formula_pretty, "material_id": mat.material_id, "band_gap": mat.band_gap, "efermi": mat.efermi, "energy_above_hull": mat.energy_above_hull}

            subdf = pd.DataFrame(subdata, index=[0])

            cand_df = pd.concat([cand_df, subdf], axis=0)

        cand_df = cand_df.reset_index(drop=True)
        cand_df["comp_atoms"] = cand_df["formula"].apply(lambda x: Substance.from_formula(x).composition)
        cand_df["sorted_keys_comp_atoms"] = cand_df["formula"].apply(lambda x: sorted(Substance.from_formula(x).composition.keys()))
        cand_df["comp_number"] = cand_df.apply(lambda row: "".join(f'{k}{row["comp_atoms"][k]}' for k in row["sorted_keys_comp_atoms"]), axis=1)

        chosen_material_list = []

        for i, subdf in cand_df.groupby("comp_number"):
            if len(subdf) > 1:
                subdf = subdf.sort_values("energy_above_hull")
                chosen_material_list.append(subdf.index[0])

            else:
                chosen_material_list.append(subdf.index[0])

        chosen_cand_df = cand_df.loc[chosen_material_list]

        chosen_cand_df = chosen_cand_df.dropna(subset=["efermi"])

        chosen_cand_df = chosen_cand_df.reset_index(drop=True)

        chosen_cand_df["new_formula"] = None

        for i in range(len(chosen_cand_df)):
            dict_keys = list(chosen_cand_df.loc[i, "comp_atoms"].keys())

            comp = ""

            for j in range(len(dict_keys)):
                element = str(periodictable.elements[dict_keys[j]])
                comp += element + str(chosen_cand_df.loc[i, "comp_atoms"][dict_keys[j]])

            chosen_cand_df.loc[i, "new_formula"] = comp

        # except Exception as e:
        # print(e)
        # print("Error: ", i, j)

        display(chosen_cand_df)

        # できたもの二つ目も保存しましょうね
        chosen_cand_df.to_csv("/workspaces/codespace_practice/candidate_material_list/" + atm + "_is_stable" + "_candidate_material_list.csv", index=False)


# %%
dict = {5: 10, 1: 11, 6: 2}
dict_key = dict.keys()
keys_list = list(dict_key)
print(keys_list)


# %%
# この得たデータをpickleで保存する理由が!ありません!
# 地産地消でcsvにしよう!
cand_df = pd.DataFrame(columns=["formula", "material_id", "band_gap", "efermi", "energy_above_hull"])
for mat in results:
    subdata = {"formula": mat.formula_pretty, "material_id": mat.material_id, "band_gap": mat.band_gap, "efermi": mat.efermi, "energy_above_hull": mat.energy_above_hull}

    subdf = pd.DataFrame(subdata, index=[0])

    cand_df = pd.concat([cand_df, subdf], axis=0)


cand_df = cand_df.reset_index(drop=True)
cand_df["comp_atoms"] = cand_df["formula"].apply(lambda x: Substance.from_formula(x).composition)
cand_df["sorted_keys_comp_atoms"] = cand_df["formula"].apply(lambda x: sorted(Substance.from_formula(x).composition.keys()))
cand_df["comp_number"] = cand_df.apply(lambda row: "".join(f'{k}{row["comp_atoms"][k]}' for k in row["sorted_keys_comp_atoms"]), axis=1)

chosen_material_list = []

for i, subdf in cand_df.groupby("comp_number"):
    if len(subdf) > 1:
        subdf = subdf.sort_values("energy_above_hull")
        chosen_material_list.append(subdf.index[0])

    else:
        chosen_material_list.append(subdf.index[0])

chosen_cand_df = cand_df.loc[chosen_material_list]

chosen_cand_df = chosen_cand_df.dropna(subset=["efermi"])

chosen_cand_df = chosen_cand_df.reset_index(drop=True)


# %%
# できたものは保存しましょうね～
# chosen_cand_df.to_csv("/workspaces/codespace_practice/candidate_material_list/candidate_material_list.csv", index=False)
# chosen_cand_df = pd.read_csv("/workspaces/codespace_practice/candidate_material_list/candidate_material_list.csv")

# どうやら一度保存してから再読み込みの形を取ると辞書型が崩れて文字型になるので以下の処理が必要
# chosen_cand_df["comp_atoms"] = chosen_cand_df["comp_atoms"].apply(ast.literal_eval)


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


display(chosen_cand_df)

# できたもの二つ目も保存しましょうね
chosen_cand_df.to_csv("/workspaces/codespace_practice/candidate_material_list/" + element_filter + "_candidate_material_list.csv", index=False)
# %%
