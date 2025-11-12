import sys
import requests
import json

FILENAME = "data.json"

# Defining main function
def main():
    if len(sys.argv) != 2:
        print("Invalid syntax, the program needs a command")
        return
    if sys.argv[1] == "highlights":
        print("Getting highights")
        getHighligths()
    elif sys.argv[1] == "detailed":
        print("Getting detailed")
        # getDetailed()
    else:
        print("The commands are 'highligts' or 'detailed'")


def getHighligths():
    url = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"
    #url = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2.json"
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        with open(FILENAME, "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True, ensure_ascii=False)

        #print(data)

        #for key in data:
        #    print(key, ":", data[key])
        
        


# Using the special variable
# __name__
if __name__=="__main__":
    main()
