#XRDで取った回折データとICSDからとったデータをグラフにして比較する
#XRDからのデータはtxt　ICSDからはcsv

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# %%
#XRDからのデータ
XRD_data = pd.read_csv("/workspaces/codespace_practice/XRD_graph/XRD_data/Li2ZnSn3O8_20240711.txt")
display(XRD_data)


#ICSDからのデータ
ICSD_data = pd.read_csv("/workspaces/codespace_practice/XRD_graph/XRD_data/Li2ZnSn3O8_xy_ICSD.csv")
display(ICSD_data)


#グラフとして見やすくするためにそれぞれの最大値をもとにスケーリング ICSDのほうがでかいのでこっちを小さくする
XRD_max = XRD_data["Intensity"].max()
ICSD_max = ICSD_data["Intensity"].max()
ICSD_data["Intensity"] = ICSD_data["Intensity"] * XRD_max / ICSD_max

# %%
#2つのデータを同じグラフに表示　X軸は10-60
plt.plot(XRD_data["2theta"], XRD_data["Intensity"], label="XRD")
plt.plot(ICSD_data["2theta"], ICSD_data["Intensity"], label="ICSD")
plt.xlabel("2Theta")
plt.ylabel("Intensity")
plt.legend()
plt.xlim(10, 60)
plt.savefig("/workspaces/codespace_practice/XRD_graph/Li2ZnSn3O8_graph.png", dpi = 300)
plt.show()

# %%
#bokehで描画
from bokeh.plotting import figure, output_file, show, save
from bokeh.models import ColumnDataSource, PanTool, WheelZoomTool, BoxZoomTool, ResetTool

source_XRD = ColumnDataSource(data=dict(x=XRD_data["2theta"], y=XRD_data["Intensity"]))
source_ICSD = ColumnDataSource(data=dict(x=ICSD_data["2theta"], y=ICSD_data["Intensity"]))

p = figure(title="XRD vs ICSD", x_axis_label='2theta', y_axis_label='Intensity', x_range=(10, 60))
p.line('x', 'y', source=source_XRD, legend_label="XRD", line_width=1, color="blue")
p.line('x', 'y', source=source_ICSD, legend_label="ICSD", line_width=1, color="red")
p.add_tools(PanTool(), WheelZoomTool(), BoxZoomTool(), ResetTool())
output_file("/workspaces/codespace_practice/XRD_graph/Li2ZnSn3O8_graph.html")
save(p)


# %%
