import time
from os.path import exists
import pandas as pd

# This class has helping methods
class Helper:

    @staticmethod
    def createDateAsString() -> str:
        lt = time.localtime()
        day = str(lt.tm_mday)
        if(int(day) < 10):
            day = "0" + day
        month = str(lt.tm_mon)
        if(int(month) < 10):
            month = "0" + month
        year = str(lt.tm_year)
        return (day + "." + month + "." + year)
        
    @staticmethod
    def createTimeAsString() -> str:
        lt = time.localtime()
        hour = str(lt.tm_hour)
        if(int(hour) < 10):
            hour = "0" + hour
        min = str(lt.tm_min)
        if(int(min) < 10):
            min = "0" + min
        return (hour + ":" + min)
    
    @staticmethod
    def getPlayerURL(id, firstname, lastname) -> str:
        base_url = "https://www.futwiz.com/en/fifa23/player/"
        url = base_url + firstname + "-" + lastname + "/" + str(id)
        return url
    
    @staticmethod
    def addDateAndTimeColumns(dataframe):
        dataframe.insert(0, "Time", Helper.createTimeAsString())
        dataframe.insert(0, "Date", Helper.createDateAsString())
        return dataframe
    
    @staticmethod
    def createDefaultHistories(player_history_path, rating_history_path):
        if(not exists(player_history_path)):
            with open(player_history_path, "w") as file:
                file.write("Date, Time, ID, Firstname, Lastname, Price\n")
        if(not exists(rating_history_path)):
                with open(rating_history_path, "w") as file:
                    file.write("Date, Time, Rating, Lowest, 2nd-Lowest, 3rd-Lowest, Average\n")

    @staticmethod
    def createNewHistory(toAdd, path):
        dataframe = pd.read_csv(path)
        if(len(dataframe) == 0):
            output = toAdd
        else:
            output = pd.concat([dataframe] + [toAdd], ignore_index=True)
        output.to_csv(path, index=False)

    @staticmethod
    def getPlayers(player_path):
        df = pd.read_csv(player_path)
        list = []

        for i in range(len(df)):
            id = df["ID"].iloc[i]
            firstname = df["Firstname"].iloc[i]
            lastname = df["Lastname"].iloc[i]
            list.append([id, firstname, lastname])

        return list
    
    @staticmethod
    def getRatings(ratings_path):
        df = pd.read_csv(ratings_path)
        list = []

        for i in range(len(df)):
            rating = df["Rating"].loc[i]
            list.append(rating)

        return list