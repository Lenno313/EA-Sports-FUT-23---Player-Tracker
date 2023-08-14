from bs4 import BeautifulSoup
from os.path import exists
import requests
import pandas as pd
import time

# ------------------------- FILES & TIME -------------------------
# Create a string with current date & time
lt = time.localtime()
day = str(lt.tm_mday)
if(int(day) < 10):
    day = "0" + day
month = str(lt.tm_mon)
if(int(month) < 10):
    month = "0" + month
year = str(lt.tm_year)
hour = str(lt.tm_hour)
if(int(hour) < 10):
    hour = "0" + hour
min = str(lt.tm_min)
if(int(min) < 10):
    min = "0" + min
date_str = day + "." + month + "." + year
time_str = hour + ":" + min

# Check if there is already a file for the history prices and put it into a DataFrame
# If not: create a new file & write in the columns
price_hist_path = "player_prices_history.csv"
if(not exists(price_hist_path)):
    with open(price_hist_path, "w") as file:
        file.write("Date, Time, ID, Firstname, Lastname, Price\n")
df_hist_prices = pd.read_csv(price_hist_path)

rating_price_hist_path = "rating_prices_history.csv"
if(not exists(rating_price_hist_path)):
    with open(rating_price_hist_path, "w") as file:
        file.write("Date, Time, Rating, Lowest, 2nd-Lowest, 3rd-Lowest, Average\n")
df_rating_hist_prices = pd.read_csv(rating_price_hist_path)

# Read the CSV-Files with the players to check
player_df = pd.read_csv("players.csv")

# --------------------- SCRAPING PLAYERS -------------------
df_cur_prices = pd.DataFrame(columns=["ID", "Firstname", "Lastname", "Price"])

base_url = "https://www.futwiz.com/en/fifa23/player/"
for i in range(len(player_df)):
    # Create the URLs for the websites by each player
    firstname = player_df.loc[i]["Firstname"]
    lastname = player_df.loc[i]["Lastname"]
    id = player_df.loc[i]["ID"]
    url = base_url + firstname + "-" + lastname + "/" + str(id)

    # Check the current price on the website
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html")

    price_div = soup.find("div", class_ = "price-num")

    price = price_div.text.replace(",", "")

    # put the rows in the DataFrame -> current prices
    df_cur_prices.loc[i] = [id, firstname, lastname, price]


# Read the CSV-Files with the players to check
rating_df = pd.read_csv("ratings.csv")

# ------------------- SCRAPING RATINGS --------------------
df_rating_cur_prices = pd.DataFrame(columns=["Rating", "Lowest", "2nd-Lowest", "3rd-Lowest", "Average"])
loc = 0
for r in rating_df["Rating"]:
    url = "https://www.futwiz.com/en/lowest-price-ratings"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html")

    right_part = soup.find("div", class_="col-9 rightContent")

    rating_parts = right_part.find_all("div", class_="col-4")
    base = 82
    index = r - 82

    rating_part = rating_parts[index]

    raw_prices = rating_part.find_all("div", class_="col-3")

    prices = []
    for p in raw_prices:
        price_text = ""
        if("K" in p.text):
            price_text = p.text.replace("\n", "").replace("K", "")
            price = float(price_text) * 1000
        if("M" in p.text):
            price_text = p.replace("\n", "").replace("M", "")
            price = float(price_text) * 1000000
        prices.append(price)

    lowest = prices[0]
    second_lowest = prices[1]
    third_lowest = prices[2]
    sum = 0.0
    for p in prices:
        sum += p
    average = sum / 10

    df_rating_cur_prices.loc[loc] = [r, lowest, second_lowest, third_lowest, average]
    loc += 1

# -------------------- SAVE HISTORY ----------------------
# Save the DataFrame of the current prices as a CSV-File
df_cur_prices.to_csv("current_prices.csv", index=False)
df_rating_cur_prices.to_csv("current_rating_prices.csv", index=False)

# Put the current prices into the history-DataFrame & save it as CSV-File
df_cur_prices.insert(0, "Time", time_str)
df_cur_prices.insert(0, "Date", date_str) 

if(len(df_hist_prices) == 0):
    new_hist_df = df_cur_prices
else:
    new_hist_df = pd.concat([df_hist_prices] + [df_cur_prices], ignore_index=True)
new_hist_df.to_csv(price_hist_path, index=False)

# Do the same for the ratings
df_rating_cur_prices.insert(0, "Time", time_str)
df_rating_cur_prices.insert(0, "Date", date_str) 

if(len(df_rating_hist_prices) == 0):
    new_rating_hist_df = df_rating_cur_prices
else:
    new_rating_hist_df = pd.concat([df_rating_hist_prices] + [df_rating_cur_prices], ignore_index=True)
new_rating_hist_df.to_csv(rating_price_hist_path, index=False)

# Run this programm every hour automatically - to get a nice history 
