import ScraperClass
import HelperClass
import pandas as pd

Helper = HelperClass.Helper
Scraper = ScraperClass.Scraper

def main():
    player_path = "players.csv"
    ratings_path = "ratings.csv"
    player_history_path = "player_history.csv"
    rating_history_path = "rating_history.csv"

    # Load DataFrames from CSV
    ratings = Helper.getRatings(ratings_path)
    players = Helper.getPlayers(player_path)

    # Scraping
    scraper = Scraper(players, ratings)
    scraper.scrape()

    # Concat with old History and save in file
    player_prices_df = Helper.addDateAndTimeColumns(scraper.getPlayerPricesDF())
    rating_prices_df = Helper.addDateAndTimeColumns(scraper.getRatingPricesDF())

    Helper.createDefaultHistories(player_history_path, rating_history_path)

    Helper.createNewHistory(player_prices_df, player_history_path)
    Helper.createNewHistory(rating_prices_df, rating_history_path)

    # check config: what the Analyzer analyze ?

# Run main method
main()