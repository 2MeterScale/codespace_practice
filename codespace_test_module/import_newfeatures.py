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

# %%
#一つのディレクトリ内の全データを読み込む
read_dir = "/workspaces/codespace_practice/train_material_list"

train_material_df = pd.DataFrame(columns = ["formula", "material_id", "band_gap", "efermi", "energy_above_hull"])

#%%
for filename in os.listdir(read_dir):
    with open(read_dir + "/" + filename, "rb") as f:
        data = pickle.load(f)
        data = pd.DataFrame(data, index=[0])
        train_material_df = pd.concat([train_material_df, data], axis=0)
train_material_df = train_material_df.reset_index(drop = True)
train_material_df["comp_atoms"] = train_material_df["formula"].apply(lambda x: Substance.from_formula(x).composition)
train_material_df["sorted_keys_comp_atoms"] = train_material_df["formula"].apply(lambda x: sorted(Substance.from_formula(x).composition.keys()))

# %%
train_material_df["comp_number"] = train_material_df.apply(lambda row: ''.join(f'{k}{row["comp_atoms"][k]}' for k in row["sorted_keys_comp_atoms"]), axis=1)

# %%
for i, subdf in train_material_df.groupby("comp_number"):
    display(subdf)
    print(len(subdf))
    break

# %%
display(train_material_df.head())