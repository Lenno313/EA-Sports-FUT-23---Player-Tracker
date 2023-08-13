import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

cur_price_path = "current_prices.csv"
hist_price_path = "prices_history.csv"

cur_df = pd.read_csv(cur_price_path)
hist_df = pd.read_csv(hist_price_path)

for id in hist_df["ID"].unique():
    df_player = hist_df[hist_df["ID"] == id]
    
    playername = df_player["Firstname"].iloc[0] + " " + df_player["Lastname"].iloc[0]
    print("-----------------|", playername, "|-----------------")
    
    # get the max & min price - with the time when the peak was
    max = df_player["Price"].max()
    df_max = df_player[df_player["Price"] == max]
    date_max = df_max["Date"].iloc[0]
    time_max = df_max["Time"].iloc[0]
    min = df_player["Price"].min()
    df_min = df_player[df_player["Price"] == min]
    date_min = df_min["Date"].iloc[0]
    time_min = df_min["Time"].iloc[0]

    # get the current price
    current = cur_df[cur_df["ID"] == id]["Price"].iloc[0]
    print("max price:", max, "-", date_max, time_max)
    print("min price:", min, "-", date_min, time_min)
    print("current price:", current)

    prices = df_player["Price"]

    # create the elements (date & time) for the x-axis
    hours = df_player["Time"]
    dates = df_player["Date"]
    moments = pd.Series("Moment")
    for i in range(len(df_player)):
        moments.loc[i] = dates.iloc[i] + " " + hours.iloc[i]

    # Create a bar-diagramm over hours (x) & the prices (y)
    hourly_graph = go.Figure(
        data = go.Bar(
            x = moments, 
            y = prices),
        layout = go.Layout(
            title = playername
        )
    )
    hourly_graph.write_html(playername + "_hist_hourly.html", auto_open = False)

    # Create a daily bar-diagramm over days (x) & prices (y)
    daily_graph = px.box(df_player, x = "Date", y="Price")
    daily_graph.write_html(playername + "_hist_daily.html", auto_open = False)

    # Next steps
    # Is the price increasing or decreasing ?
    # View the last hours, days & weeks
    # 24 hours -> count the "ups" & downs and look at the start / end