# %%
import pandas as pd
import pickle
from chempy import Substance
import os

#現状のプログラム作成方針
#ver.3の組成式ファイルの中にあるnew_formulaをもとにして取得した物質情報から2つの情報を抜き出す
#今回はそもファイルの個数自体があまり多くないので、毎行ごとにすべてのデータに参照をかける形でやっていきたいと考えている
#ただし、一つの化合物に対していくつかの物質ファイルが存在する場合があるので、その場合の対処法を決定する必要がある　
#少なくとも平均を取るのはよくないと考えるので大きいか小さいかのどちらかに集中して訂正する必要がある
#まずはいったん一番低いやつを採用するかな…

#天才アイデア～train_material_listにある情報全部読み込んで一個のデータフレームにすればいいじゃんね



# %% これは追加するmaterials projectのデータ成型用
#一つのディレクトリ内の全データを読み込む
read_dir = "/workspaces/codespace_practice/train_material_list"

train_material_df = pd.DataFrame(columns = ["formula", "material_id", "band_gap", "efermi", "energy_above_hull"])

for filename in os.listdir(read_dir):
    with open(read_dir + "/" + filename, "rb") as f:
        data = pickle.load(f)
        data = pd.DataFrame(data, index=[0])
        train_material_df = pd.concat([train_material_df, data], axis=0)
train_material_df = train_material_df.reset_index(drop = True)
train_material_df["comp_atoms"] = train_material_df["formula"].apply(lambda x: Substance.from_formula(x).composition)
train_material_df["sorted_keys_comp_atoms"] = train_material_df["formula"].apply(lambda x: sorted(Substance.from_formula(x).composition.keys()))
train_material_df["comp_number"] = train_material_df.apply(lambda row: ''.join(f'{k}{row["comp_atoms"][k]}' for k in row["sorted_keys_comp_atoms"]), axis=1)

chosen_material_list = []

for i, subdf in train_material_df.groupby("comp_number"):
    if len(subdf) > 1:
        subdf = subdf.sort_values("energy_above_hull")
        chosen_material_list.append(subdf.index[0])
        
    else:
        chosen_material_list.append(subdf.index[0])

chosen_train_material_df = train_material_df.loc[chosen_material_list]



# %% ver3を読み込んで構成元素の数字情報を作成
SC_data = pd.read_csv("/workspaces/codespace_practice/codespace_test_module/final_SC_X_data_ver3.csv")
SC_data = SC_data.dropna(subset=["new_formula"])
SC_data = SC_data.reset_index(drop = True)
SC_data["new_formula"] = SC_data["new_formula"].astype(str)
SC_data["comp_atoms"] = SC_data["new_formula"].apply(lambda x: Substance.from_formula(x).composition)
SC_data["sorted_keys_comp_atoms"] = SC_data["new_formula"].apply(lambda x: sorted(Substance.from_formula(x).composition.keys()))
SC_data["comp_number"] = SC_data.apply(lambda row: ''.join(f'{k}{row["comp_atoms"][k]}' for k in row["sorted_keys_comp_atoms"]), axis=1)



# %% 二つのdfが用意できたので、これらのdfをもとに各ver3のほうのcomp_numberと
#一致するmatproj側のfermiデータやらなんやらを足し合わせてNNモデルに突っ込む
SC_data["efermi"] = None
SC_data["band_gap"] = None
for i in range(len(SC_data)):
    if SC_data.loc[i, "comp_number"] in chosen_train_material_df["comp_number"].values:
        #print(chosen_train_material_df.loc[chosen_train_material_df["comp_number"].values == SC_data.loc[i, "comp_number"], "efermi"].values)
        SC_data.loc[i, "efermi"] = chosen_train_material_df.loc[chosen_train_material_df["comp_number"].values == SC_data.loc[i, "comp_number"], "efermi"].values
        SC_data.loc[i, "band_gap"] = chosen_train_material_df.loc[chosen_train_material_df["comp_number"].values == SC_data.loc[i, "comp_number"], "band_gap"].values
    else:
        SC_data.loc[i, "efermi"] = None
        SC_data.loc[i, "band_gap"] = None


# %%
SC_data = SC_data.dropna(subset=["efermi", "band_gap"])
display(SC_data)


#%%
display(SC_data.loc[SC_data["band_gap"] != 0.0, ["new_formula", "band_gap"]])


# %%
SC_data.to_csv("/workspaces/codespace_practice/codespace_test_module/CrabNet_train_data.csv", index=False)
# %%
