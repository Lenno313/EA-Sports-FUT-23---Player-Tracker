import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from os.path import exists

players_path = "players.csv"
ratings_path = "ratings.csv"
player_history_path = "player_history.csv"
rating_history_path = "rating_history.csv"

player_df = pd.read_csv(players_path)
ratings_df = pd.read_csv(ratings_path)
player_history_df = pd.read_csv(player_history_path)
rating_history_df = pd.read_csv(rating_history_path)

with open("status.txt", "w") as file:
    file.write("Investitionen in Spieler")
    output = ""
    profit_all = 0.0
    value_all = 0.0
    for id in player_df["ID"].unique():
        cost_data = player_df[player_df["ID"] == id]
        firstname = cost_data["Firstname"].iloc[0]
        lastname = cost_data["Lastname"].iloc[0]
        current_data = player_history_df[player_history_df["ID"] == id]

        amount = cost_data["Amount"].iloc[0]
        cost_pp = cost_data["CostPP"].iloc[0]
        cost = amount * cost_pp
        current_price = current_data.iloc[0]["Price"]
        current_value = current_price * amount
        value_all += current_value
        profit = current_value * 0.95 - cost
        profit_all += profit

        line1 = firstname[0].upper() + firstname[1::] + " " + lastname[0].upper() + lastname[1::] + ":"
        line2 = "Anzahl: " + amount.astype(str) + " | Preis pro Spieler: " + cost_pp.astype(str) + " | Kosten gesamt: " + cost.astype(str)
        line3 = "Aktueller Preis: " + current_price.astype(str) + " | Wert gesamt (brutto): " + current_value.astype(str)
        line4 = "Aktueller Profit / Verlust (netto): " + profit.astype(str)
        output = "\n \n" + line1 + "\n" + line2 + "\n" + line3 + "\n" + line4

        file.write(output)

    file.write("\n \n" + "Investitionen in Rating")

    for rating in ratings_df["Rating"]:
        cost_data = ratings_df[ratings_df["Rating"] == rating]
        current_data = rating_history_df[rating_history_df["Rating"] == rating]

        amount = cost_data["Amount"].iloc[0]
        cost_pp = cost_data["CostPP"].iloc[0]
        cost = amount * cost_pp
        current_price = current_data.iloc[0]["2nd-Lowest"]
        current_value = current_price * amount
        value_all += current_value
        profit = current_value * 0.95 - cost
        profit_all += profit

        line1 = str(rating) + "er"
        line2 = "Anzahl: " + amount.astype(str) + " | Preis pro Spieler: " + cost_pp.astype(str) + " | Kosten gesamt: " + cost.astype(str)
        line3 = "Aktueller Preis (2.niedrigster): " + current_price.astype(str) + " | Wert gesamt (brutto): " + current_value.astype(str)
        line4 = "Aktueller Profit / Verlust (netto): " + profit.astype(str)
        output = "\n \n" + line1 + "\n" + line2 + "\n" + line3 + "\n" + line4

        file.write(output)
    file.write("\n \n \n" + "AKTUELLER PROFIT INSGESAMT: " + profit_all.astype(str) + "\n")
    file.write("AKTUELLER WERT INSGESAMT: " + value_all.astype(str) + "\n")











"""
cur_price_path = "current_prices.csv"
hist_price_path = "player_prices_history.csv"

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

"""