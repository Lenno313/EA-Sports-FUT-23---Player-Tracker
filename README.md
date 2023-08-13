# EA Sports FUT 23 - Ü Tracker
 In this project, I will get and analyze the prices of given players from FUTWIZ

If you visit the FUTWIZ Website and choose a player the website tells you the current price of the player:

![FUTWIZ Website](futwiz-messi-page.PNG "FUTWIZ")

For the URL of the player's website you just need:
- the ID of the player
- the first name of the player
- the last name of the player
https://www.futwiz.com/en//fifa23/player/lionel-messi/51

So in the next step, I create a CSV-File with the players which I want to check the price from:

![Player.csv](player-file.PNG "Player file")

Now with the information about the player we can start the Web scraping:
The first Python script pulls the prices of the players and put them into a DataFrame
Then it saves the newest prices into the "current_prices.csv" file

![current-prices-csv](current-prices.png "Player price")

Also, it appends the prices to the "price_history" which has the additional columns:
- Date
- Time

![prices-history-csv](prices-history.png "Player history")
  
