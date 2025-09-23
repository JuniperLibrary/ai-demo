import pandas as pd
df = pd.read_csv("beike_wanfui_jade_xq.csv", parse_dates=["timestamp"])
df.set_index("timestamp", inplace=True)
df["avg_price"].plot(title="万科翡翠 小区参考均价", ylabel="元/㎡")
