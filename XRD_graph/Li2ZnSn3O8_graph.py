# XRDで取った回折データとICSDからとったデータをグラフにして比較する
# XRDからのデータはtxt　ICSDからはcsv

# %%
import matplotlib.pyplot as plt
import pandas as pd
from bokeh.models import ColumnDataSource, CrosshairTool, HoverTool, Range1d, RedoTool, UndoTool
from bokeh.plotting import figure, output_file, save

# %%
# XRDからのデータ
XRD_data = pd.read_csv("/workspaces/codespace_practice/XRD_graph/XRD_data/Li2ZnSn3O8_20240711.txt")

XRD_doped_data = pd.read_csv("/workspaces/codespace_practice/XRD_graph/XRD_data/Li2.5Zn0.8Ga0.2Sn3O8_20241017.txt")

#二度焼きのデータ
XRD_2doyaki_data = pd.read_csv("/workspaces/codespace_practice/XRD_graph/XRD_data/Li2ZnSn3O8_2ndyaki_20241022.txt")

#Li多め単体のデータ
XRD_moreLi_data = pd.read_csv("/workspaces/codespace_practice/XRD_graph/XRD_data/Li2.5ZnSn3O8_20241112.txt")

# ICSDからのデータ
ICSD_data = pd.read_csv("/workspaces/codespace_practice/XRD_graph/XRD_data/Li2ZnSn3O8_xy_ICSD.csv")
ICSD_SnO2_data = pd.read_csv("/workspaces/codespace_practice/XRD_graph/XRD_data/SnO2_xy_ICSD.csv")
ICSD_ZnO_data = pd.read_csv("/workspaces/codespace_practice/XRD_graph/XRD_data/ZnO_xy_ICSD.csv")
ICSD_Zn2SnO4_data = pd.read_csv("/workspaces/codespace_practice/XRD_graph/XRD_data/Zn2SnO4_xy_ICSD.csv")
ICSD_Li2SnO3_data = pd.read_csv("/workspaces/codespace_practice/XRD_graph/XRD_data/Li2SnO3_xy_ICSD.csv")
ICSD_Li2O2_data = pd.read_csv("/workspaces/codespace_practice/XRD_graph/XRD_data/Li2O2_xy_ICSD.csv")
ICSD_Li16Zn16Sn28O8_data = pd.read_csv("/workspaces/codespace_practice/XRD_graph/XRD_data/Li1.6Zn1.6Sn2.8O8_xy_ICSD.csv")

# ICSDのLi2ZnSn3O8のデータについて、offset-0.22
ICSD_data["2theta"] = [x - 0.22 for x in ICSD_data["2theta"]]
ICSD_Li16Zn16Sn28O8_data["2theta"] = [x - 0.12 for x in ICSD_Li16Zn16Sn28O8_data["2theta"]]
# SnO2のデータについてoffset-0.08
ICSD_SnO2_data["2theta"] = [x - 0.08 for x in ICSD_SnO2_data["2theta"]]

# グラフとして見やすくするためにそれぞれの最大値をもとにスケーリング ICSDのほうがでかいのでこっちを小さくする
XRD_max = XRD_data["Intensity"].max()
XRD_doped_max = XRD_doped_data["Intensity"].max()
XRD_2doyaki_max = XRD_2doyaki_data["Intensity"].max()
XRD_moreLi_max = XRD_moreLi_data["Intensity"].max()
ICSD_max = ICSD_data["Intensity"].max()
ICSD_SnO2_max = ICSD_SnO2_data["Intensity"].max()
ICSD_ZnO_max = ICSD_ZnO_data["Intensity"].max()
ICSD_Zn2SnO4_max = ICSD_Zn2SnO4_data["Intensity"].max()
ICSD_Li2SnO3_max = ICSD_Li2SnO3_data["Intensity"].max()
ICSD_Li2O2_max = ICSD_Li2O2_data["Intensity"].max()
ICSD_Li16Zn16Sn28O8_max = ICSD_Li16Zn16Sn28O8_data["Intensity"].max()

XRD_doped_data["Intensity"] = XRD_doped_data["Intensity"] * XRD_max / XRD_doped_max
XRD_2doyaki_data["Intensity"] = XRD_2doyaki_data["Intensity"] * XRD_max / XRD_2doyaki_max
XRD_moreLi_data["Intensity"] = XRD_moreLi_data["Intensity"] * XRD_max / XRD_moreLi_max
ICSD_data["Intensity"] = ICSD_data["Intensity"] * XRD_max / ICSD_max
ICSD_SnO2_data["Intensity"] = ICSD_SnO2_data["Intensity"] * 63.3333 / ICSD_SnO2_max
ICSD_ZnO_data["Intensity"] = ICSD_ZnO_data["Intensity"] * 17.5 / ICSD_ZnO_max
ICSD_Zn2SnO4_data["Intensity"] = ICSD_Zn2SnO4_data["Intensity"] * XRD_max / ICSD_Zn2SnO4_max
ICSD_Li2SnO3_data["Intensity"] = ICSD_Li2SnO3_data["Intensity"] * XRD_max / ICSD_Li2SnO3_max
ICSD_Li2O2_data["Intensity"] = ICSD_Li2O2_data["Intensity"] * XRD_max / ICSD_Li2O2_max
ICSD_Li16Zn16Sn28O8_data["Intensity"] = ICSD_Li16Zn16Sn28O8_data["Intensity"] * XRD_max / ICSD_Li16Zn16Sn28O8_max

# %%
# 2つのデータを同じグラフに表示　X軸は10-60 現状使わない
plt.plot(XRD_data["2theta"], XRD_data["Intensity"], label="XRD")
plt.plot(ICSD_data["2theta"], ICSD_data["Intensity"], label="ICSD")
plt.xlabel("2Theta")
plt.ylabel("Intensity")
plt.legend()
plt.xlim(10, 60)
plt.savefig("/workspaces/codespace_practice/XRD_graph/Li2ZnSn3O8_graph.png", dpi=300)
plt.show()

# %%
# bokehで描画 他ICSDのデータとの比較
# 目的は物質が出来ているかどうか

# Li2.5Zn0.8Ga0.2Sn3O8のデータについてoffset-0.08
XRD_doped_data["2theta"] = [x - 0.08 for x in XRD_doped_data["2theta"]]

source_XRD = ColumnDataSource(data=dict(x=XRD_data["2theta"], y=XRD_data["Intensity"]))
source_XRD_doped = ColumnDataSource(data=dict(x=XRD_doped_data["2theta"], y=XRD_doped_data["Intensity"]))
source_XRD_2doyaki = ColumnDataSource(data=dict(x=XRD_2doyaki_data["2theta"], y=XRD_2doyaki_data["Intensity"]))
source_XRD_moreLi = ColumnDataSource(data=dict(x=XRD_moreLi_data["2theta"], y=XRD_moreLi_data["Intensity"]))
source_ICSD = ColumnDataSource(data=dict(x=ICSD_data["2theta"], y=ICSD_data["Intensity"]))
source_ICSD_SnO2 = ColumnDataSource(data=dict(x=ICSD_SnO2_data["2theta"], y=ICSD_SnO2_data["Intensity"]))
source_ICSD_ZnO = ColumnDataSource(data=dict(x=ICSD_ZnO_data["2theta"], y=ICSD_ZnO_data["Intensity"]))
source_ICSD_Zn2SnO4 = ColumnDataSource(data=dict(x=ICSD_Zn2SnO4_data["2theta"], y=ICSD_Zn2SnO4_data["Intensity"]))
source_ICSD_Li2SnO3 = ColumnDataSource(data=dict(x=ICSD_Li2SnO3_data["2theta"], y=ICSD_Li2SnO3_data["Intensity"]))
source_ICSD_Li2O2 = ColumnDataSource(data=dict(x=ICSD_Li2O2_data["2theta"], y=ICSD_Li2O2_data["Intensity"]))
source_ICSD_Li16Zn16Sn28O8 = ColumnDataSource(data=dict(x=ICSD_Li16Zn16Sn28O8_data["2theta"], y=ICSD_Li16Zn16Sn28O8_data["Intensity"]))

# グラフの範囲を設定
x_range = Range1d(start=10, end=60, bounds=(10, 60))
y_range = Range1d(start=0, end=XRD_max * 1.1, bounds="auto")
p = figure(title="Li2ZnSn3O8 XRD data", x_axis_label="2theta", y_axis_label="Intensity", x_range=x_range, width=1200, height=400, y_range=y_range)

p.line("x", "y", source=source_XRD, legend_label="XRD_Li2ZnSn3O8", line_width=1, color="blue")
p.line("x", "y", source=source_XRD_doped, legend_label="XRD_Li2.5Zn0.8Ga0.2Sn3O8", line_width=1, color="yellow")
#p.line("x", "y", source=source_XRD_2doyaki, legend_label="XRD_Li2ZnSn3O8_2ndyaki", line_width=1, color="orange")
p.line("x", "y", source=source_XRD_moreLi, legend_label="XRD_Li2.5ZnSn3O8", line_width=1, color="green")
p.line("x", "y", source=source_ICSD, legend_label="ICSD_Li2ZnSn3O8", line_width=1, color="red")
#p.line("x", "y", source=source_ICSD_SnO2, legend_label="ICSD_SnO2", line_width=1, color="green")
#p.line("x", "y", source=source_ICSD_ZnO, legend_label="ICSD_ZnO", line_width=1, color="purple")
# p.line("x", "y", source=source_ICSD_Zn2SnO4, legend_label="ICSD_Zn2SnO4", line_width=1, color="orange")
# p.line("x", "y", source=source_ICSD_Li2SnO3, legend_label="ICSD_Li2SnO3", line_width=1, color="orange")
#p.line("x", "y", source=source_ICSD_Li2O2, legend_label="ICSD_Li2O2", line_width=1, color="orange")
# p.line("x", "y", source=source_ICSD_Li16Zn16Sn28O8, legend_label="ICSD_Li1.6Zn1.6Sn2.8O8", line_width=1, color="orange")

p.add_tools(HoverTool(), CrosshairTool(), UndoTool(), RedoTool())
p.legend.click_policy = "hide"

output_file("/workspaces/codespace_practice/XRD_graph/Li2.5ZnGaSn3O8_Ga_graph_20241112.html")
save(p)

# %%
# ドープ・ずれの確認
XRD_doped_data_copy = XRD_doped_data.copy()
XRD_doped_data_copy["2theta"] = [x - 0.08 for x in XRD_doped_data_copy["2theta"]]
XRD_2doyaki_data_copy = XRD_2doyaki_data.copy()
XRD_2doyaki_data_copy["2theta"] = [x - 0.14 for x in XRD_2doyaki_data_copy["2theta"]]

source_XRD = ColumnDataSource(data=dict(x=XRD_data["2theta"], y=XRD_data["Intensity"]))
source_XRD_doped_copy = ColumnDataSource(data=dict(x=XRD_doped_data_copy["2theta"], y=XRD_doped_data_copy["Intensity"]))
source_XRD_2doyaki_copy = ColumnDataSource(data=dict(x=XRD_2doyaki_data_copy["2theta"], y=XRD_2doyaki_data_copy["Intensity"]))


# グラフの範囲を設定
x_range = Range1d(start=10, end=60, bounds=(10, 60))
y_range = Range1d(start=0, end=XRD_max * 1.1, bounds="auto")
p = figure(title="Li2ZnSn3O8 XRD data", x_axis_label="2theta", y_axis_label="Intensity", x_range=x_range, width=1200, height=400, y_range=y_range)

#p.line("x", "y", source=source_XRD, legend_label="XRD_Li2ZnSn3O8", line_width=1, color="blue")
p.line("x", "y", source=source_XRD_doped_copy, legend_label="XRD_Li2.5Zn0.8Ga0.2Sn3O8", line_width=1, color="yellow")
p.line("x", "y", source=source_XRD_2doyaki_copy, legend_label="XRD_Li2ZnSn3O8_2ndyaki", line_width=1, color="red")

p.add_tools(HoverTool(), CrosshairTool(), UndoTool(), RedoTool())
p.legend.click_policy = "hide"

output_file("/workspaces/codespace_practice/XRD_graph/Li2ZnSn3O8_dopecheck_graph_20241017.html")
save(p)
# %%
