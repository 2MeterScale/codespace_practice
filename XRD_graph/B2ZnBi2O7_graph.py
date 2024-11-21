# XRDで取った回折データとICSDからとったデータをグラフにして比較する
# XRDからのデータはtxt　ICSDからはcsv

# %%
import pandas as pd
from bokeh.models import ColumnDataSource, CrosshairTool, HoverTool, Range1d, RedoTool, UndoTool
from bokeh.plotting import figure, output_file, save

# %%
# XRDからのデータ
XRD_data = pd.read_csv("/workspaces/codespace_practice/XRD_graph/XRD_data/B2ZnBi2O7.txt")

XRD_data_2kome = pd.read_csv("/workspaces/codespace_practice/XRD_graph/XRD_data/B2ZnBi2O7_2kome.txt")

# ICSDからのデータ
ICSD_data = pd.read_csv("/workspaces/codespace_practice/XRD_graph/XRD_data/B2ZnBi2O7_xy_ICSD.csv")

# グラフとして見やすくするためにそれぞれの最大値をもとにスケーリング ICSDのほうがでかいのでこっちを小さくする
XRD_max = XRD_data["Intensity"].max()

XRD_2kome_max = XRD_data_2kome["Intensity"].max()

ICSD_max = ICSD_data["Intensity"].max()

ICSD_data["Intensity"] = ICSD_data["Intensity"] * XRD_max / ICSD_max

XRD_data_2kome = XRD_data_2kome["Intensity"] * XRD_max / XRD_2kome_max


# %%
# bokehで描画 他ICSDのデータとの比較
# 目的は物質が出来ているかどうか

source_XRD = ColumnDataSource(data=dict(x=XRD_data["2theta"], y=XRD_data["Intensity"]))
source_ICSD = ColumnDataSource(data=dict(x=ICSD_data["2theta"], y=ICSD_data["Intensity"]))
source_XRD_2kome = ColumnDataSource(data=dict(x=XRD_data_2kome["2theta"], y=XRD_data_2kome["Intensity"]))


# グラフの範囲を設定
x_range = Range1d(start=10, end=60, bounds=(10, 60))
y_range = Range1d(start=0, end=XRD_max * 1.1, bounds="auto")
p = figure(title="B2ZnBi2O7 XRD data", x_axis_label="2theta", y_axis_label="Intensity", x_range=x_range, width=1200, height=400, y_range=y_range)

p.line("x", "y", source=source_XRD, legend_label="XRD_B2ZnBi2O7", line_width=1, color="blue")
p.line("x", "y", source=source_ICSD, legend_label="ICSD_B2ZnBi2O7", line_width=1, color="red")
p.line("x", "y", source=source_XRD_2kome, legend_label="XRD_B2ZnBi2O7_2kome", line_width=1, color="green")

p.add_tools(HoverTool(), CrosshairTool(), UndoTool(), RedoTool())
p.legend.click_policy = "hide"

output_file("/workspaces/codespace_practice/XRD_graph/B2ZnBi2O7_1kome_2kome_hikaku.html")
save(p)
# %%
print(XRD_data)
# %%
