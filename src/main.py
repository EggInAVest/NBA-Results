import sys
import requests
import json
import http.client

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

FILENAME = "data.json"


# Defining main function
def main():
    print(f"\n======    {bcolors.BOLD}{bcolors.OKBLUE}N{bcolors.ENDC}B{bcolors.BOLD}{bcolors.FAIL}A{bcolors.ENDC} STATS     ======")
    #while (True):
    print("\nPlease choose...\n")
    num = input("1. Last nights results (Overview)\n"
                "2. Last nights results (Detailed)\n"
                "3. Standings\n"
                "4. Season leaders\n"
                "5. EXIT\n\n")
    if (int(num) == 1):
        getGameStats()
    elif (int(num) == 2):
        getDetailedStats()
    elif (int(num) == 3):
        getStandings()
    #elif (int(num) == 4):
        #getLeaders()
    elif (int(num) == 5):
        print("Good bye!")
        exit()
    else:
        print("Invalid input\n")

"""         if len(sys.argv) == 1:
            getGameStats()
        elif len(sys.argv) == 2 and sys.argv[1] == "details":
            print("Details")
            #getDetailed()
        else:
            print("Either no arguments or 'detailed'") """




def getGameStats():
    url = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # If I want the actual JSON file to check through
        with open(FILENAME, "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True, ensure_ascii=False)
        games = data["scoreboard"]["games"]
        for game in games:
            awayCity = game["awayTeam"]["teamCity"]
            homeCity = game["homeTeam"]["teamCity"]
            awayTeam = game["awayTeam"]["teamName"]
            homeTeam = game["homeTeam"]["teamName"]
            awayScore = game["awayTeam"]["score"]
            homeScore = game["homeTeam"]["score"]
            left = f"{awayCity} {awayTeam}"
            right = f"{homeCity} {homeTeam}"
            left_padded = f"{left:<25}"
            right_padded = f"{right:<10}"

            if awayScore > homeScore:
                left_out = f"{bcolors.OKGREEN}{left_padded}{bcolors.ENDC}"
                right_out = f"{bcolors.FAIL}{right_padded}{bcolors.ENDC}"
            elif homeScore > awayScore:
                left_out = f"{bcolors.FAIL}{left_padded}{bcolors.ENDC}"
                right_out = f"{bcolors.OKGREEN}{right_padded}{bcolors.ENDC}"
            else:
                left_out = left_padded
                right_out = right_padded

            print(f"{left_out} {awayScore:>3} - {homeScore:<10} {right_out}")

def getDetailedStats():
    scoreboardUrl = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"
    response = requests.get(scoreboardUrl)
    if (response.status_code == 200):
        scoreData = response.json()
        games = scoreData["scoreboard"]["games"]
        for game in games:
            gameId = game["gameId"]
            boxScoreUrl = f"https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{gameId}.json"
            boxResponse = requests.get(boxScoreUrl)
            print(boxResponse)
            if boxResponse.status_code == 200:
                boxData = boxResponse.json()
                with open(FILENAME, "w", encoding="utf-8") as outfile:
                    json.dump(boxData, outfile, indent=4, sort_keys=True, ensure_ascii=False)

def getStandings():
    url = "https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2025/00_standings.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        with open(FILENAME, "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True, ensure_ascii=False)



# Using the special variable
# __name__
if __name__=="__main__":
    main()
