# %%
import pandas as pd
import pickle


# %%
SC_data = pd.read_csv("/workspaces/codespace_practice/codespace_test_module/final_SC_X_data_ver3.csv")

data = SC_data.loc[SC_data["new_formula"] == "Y1Ba2Cu3O7", :]
# %%
display(data)
# %%
