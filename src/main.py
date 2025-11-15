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
FILENAME2 = "players.json"


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
        gameCount = 0
        for game in games:
            gameId = game["gameId"]
            boxScoreUrl = f"https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{gameId}.json"
            boxResponse = requests.get(boxScoreUrl)
            if boxResponse.status_code == 200:
                gameCount += 1
                boxData = boxResponse.json()
                with open(FILENAME2, "w", encoding="utf-8") as outfile:
                    json.dump(boxData, outfile, indent=4, sort_keys=True, ensure_ascii=False)
                awayTeam = boxData["game"]["awayTeam"]
                awayTeamCode = awayTeam["teamTricode"]
                homeTeam = boxData["game"]["homeTeam"]
                homeTeamCode = homeTeam["teamTricode"]
                awayTeamScore = awayTeam["score"]
                homeTeamScore = homeTeam["score"]

                awayStatus = "W" if awayTeamScore > homeTeamScore else "L"
                homeStatus = "W" if homeTeamScore > awayTeamScore else "L"

                print(f"AWAY TEAM {awayTeamCode} {awayTeamScore} {awayStatus}\n")
                print(f"{'NAME':<20} {'PTS':>4} {'REB':>4} {'AST':>4} {'BLK':>4} {'STL':>4} {'TO':>4} {'FG':>8} {'3P':>8} {'FG%':>6}")
                for player in awayTeam["players"]:
                    name = player["name"]
                    status = player.get("status", "")
                    played = player.get("played", "0")
                    if status == "ACTIVE" and played == "1":
                        points = player["statistics"]["points"]
                        rebounds = player["statistics"]["reboundsTotal"]
                        assists = player["statistics"]["assists"]
                        blocks = player["statistics"]["blocks"]
                        steals = player["statistics"]["steals"]
                        turnovers = player["statistics"]["turnovers"]
                        FGM = player["statistics"]["fieldGoalsMade"]
                        FGA = player["statistics"]["fieldGoalsAttempted"]
                        FG = str(FGM) + "/" + str(FGA)
                        TPM = player["statistics"]["threePointersMade"]
                        TPA = player["statistics"]["threePointersAttempted"]
                        threes = str(TPM) + "/" + str(TPA)
                        FGP = player["statistics"]["fieldGoalsPercentage"]
                        FGP = FGP * 100
                        FGP = round(FGP, 2)
                        print(f"{name:<20} {points:>4} {rebounds:>4} {assists:>4} {blocks:>4} {steals:>4} {turnovers:>4} {FG:>8} {threes:>8} {FGP:>6}")
                    else:
                        reason = player.get("notPlayingReason", "DID NOT PLAY")
                        print(f"{name:<20}   DNP {reason}")
                print()
                print(f"HOME TEAM {homeTeamCode} {homeTeamScore} {homeStatus}\n")
                print(f"{'NAME':<20} {'PTS':>4} {'REB':>4} {'AST':>4} {'BLK':>4} {'STL':>4} {'TO':>4} {'FG':>8} {'3P':>8} {'FG%':>6}")
                for player in homeTeam["players"]:
                    name = player["name"]
                    status = player.get("status", "")
                    played = player.get("played", "0")
                    if status == "ACTIVE" and played == "1":
                        points = player["statistics"]["points"]
                        rebounds = player["statistics"]["reboundsTotal"]
                        assists = player["statistics"]["assists"]
                        blocks = player["statistics"]["blocks"]
                        steals = player["statistics"]["steals"]
                        turnovers = player["statistics"]["turnovers"]
                        FGM = player["statistics"]["fieldGoalsMade"]
                        FGA = player["statistics"]["fieldGoalsAttempted"]
                        FG = str(FGM) + "/" + str(FGA)
                        TPM = player["statistics"]["threePointersMade"]
                        TPA = player["statistics"]["threePointersAttempted"]
                        threes = str(TPM) + "/" + str(TPA)
                        FGP = player["statistics"]["fieldGoalsPercentage"]
                        FGP = FGP * 100
                        FGP = round(FGP, 2)
                        print(f"{name:<20} {points:>4} {rebounds:>4} {assists:>4} {blocks:>4} {steals:>4} {turnovers:>4} {FG:>8} {threes:>8} {FGP:>6}")
                    else:
                        reason = player.get("notPlayingReason", "DID NOT PLAY")
                        print(f"{name:<20}   DNP {reason}")
                print(80 * "-")

				#mostPoints
                #mostRebounds
                #mostAssists

   

def getStandings():

    class Team:
        def __init__(self, name, wins, losses):
            self.name = name
            self.wins = wins
            self.losses = losses
    
    URL = "https://stats.nba.com/stats/leaguestandingsv3"

    PARAMS = {
        "LeagueID": "00",
        "Season": "2025-26",
        "SeasonType": "Regular Season",
    }

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.nba.com/",
        "Origin": "https://www.nba.com",
    }

    resp = requests.get(URL, params=PARAMS, headers=HEADERS)

    if resp.status_code == 200:
        data = resp.json()
        # Save once so you can explore the structure
        with open("standings.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)
        headers = data["resultSets"][0]["headers"]
        rows = data["resultSets"][0]["rowSet"]
        
        eastTeams = []
        westTeams = []

        for row in rows:
            teamName = row[3] + " " + row[4]
            teamWins = row[13]
            teamLosses = row[14]
            team = Team(teamName, teamWins, teamLosses)
            if row[6] == "West":
                westTeams.append(team)
            else:
                eastTeams.append(team)
        westTeams.sort(key=lambda x: x.wins, reverse=True)
        eastTeams.sort(key=lambda x: x.wins, reverse=True)

        print("Western Conference\n")
        for team in westTeams:
            print(f"{team.name:<24} {team.wins:>4} - {team.losses}")
        print()
        print("Easter Conference\n")
        for team in eastTeams:
            print(f"{team.name:<24} {team.wins:>4} - {team.losses}")
    else:
        print(resp.text[:500])

"""     url = "http://rest.nbaapi.com/v1/standings"
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        with open(FILENAME, "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True, ensure_ascii=False) """



# Using the special variable
# __name__
if __name__=="__main__":
    main()
