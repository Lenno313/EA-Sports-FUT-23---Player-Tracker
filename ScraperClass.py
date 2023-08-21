import requests
from bs4 import BeautifulSoup
import HelperClass
import pandas as pd

Helper = HelperClass.Helper

# This class pulls the prices from the website and puts it into DataFrames
class Scraper:
    
    def __init__(self, player_tuples, ratings) -> None:
        self.player_tuples = player_tuples
        self.ratings = ratings
        self.rating_prices_df = pd.DataFrame(columns=["Rating", "Lowest", "2nd-Lowest", "3rd-Lowest", "Average"])
        self.player_prices_df = pd.DataFrame(columns=["ID", "Firstname", "Lastname", "Price"])

    # get 10 lowest prices by rating and return
    def scrapeRating(self, rating):
        url = "https://www.futwiz.com/en/lowest-price-ratings"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html")

        right_part = soup.find("div", class_="col-9 rightContent")

        rating_parts = right_part.find_all("div", class_="col-4")
        base = 82
        index = rating - 82

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
        return prices

    # Get price by player and return
    def scrapePlayer(self, url) -> int:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html")

        price_div = soup.find("div", class_ = "price-num")

        price = price_div.text.replace(",", "")
        return price
    
    # get the price by every player & rating | put them into a DataFrame
    def scrape(self):
        loc = 0
        for tuple in self.player_tuples:
            id = tuple[0]
            firstname = tuple[1]
            lastname = tuple[2]
            url = Helper.getPlayerURL(id, firstname, lastname)
            price = self.scrapePlayer(url)
            self.addPlayerToDF(id, firstname, lastname, price, loc)
            loc += 1

        for rating in self.ratings:
            prices = self.scrapeRating(rating)
            lowest = prices[0]
            second_lowest = prices[1]
            third_lowest = prices[2]
            sum = 0.0
            for p in prices:
                sum += p
            average = sum / 10
            self.addRatingToDF(rating, lowest, second_lowest, third_lowest, average, loc)
            loc += 1

    def addPlayerToDF(self, id, firstname, lastname, price, loc):
        self.player_prices_df.loc[loc] = [id, firstname, lastname, price]

    def addRatingToDF(self, r, lowest, second_lowest, third_lowest, average, loc):
        self.rating_prices_df.loc[loc] = [r, lowest, second_lowest, third_lowest, average]

    def getPlayerPricesDF(self):
        return self.player_prices_df
    
    def getRatingPricesDF(self):
        return self.rating_prices_df